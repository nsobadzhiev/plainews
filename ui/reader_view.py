import logging
import webbrowser
from datetime import datetime
from typing import cast

from textual import on
from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option
from textual.worker import Worker, WorkerState
from rich.table import Table

from ai.tts import speak_text, TextToSpeech, has_tts_setup
from config.config import Config
from model.article import Article
from model.feed import Feed, FeedEntry
from model.feed_manager import FeedManager
from model.session_manager import SessionManager
from model.opml import generate_opml
from transform.article_summary import ArticleSummary
from transform.article_translator import ArticleTranslator
from rich.text import Text
from ui.article_view import ArticleView
from ui.articles_list import ArticlesList
from ui.config_file_screen import ConfigFileScreen
from ui.config_file_view import ConfigFileView
from ui.feeds_list import FeedsList
from ui.latest_articles_screen import LatestArticlesScreen

logger = logging.getLogger(__name__)


class ReaderView(Widget):

    CSS_PATH = ['reader_view.tcss', 'article_layout.tcss']

    BINDINGS = [
        ("r", "refresh_feeds", "Refresh"),
        ("e", "export_feeds", "Export feeds"),
    ]

    config = Config()
    feed_manager = FeedManager()
    session_manager = SessionManager()

    def __init__(
            self,
            *children: Widget,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self.plainews = cast("Plainews", self.app)
        self.selected_feed: Feed | None = None
        self.selected_entry: FeedEntry | None = None
        self.selected_article: Article | None = None
        self.tts: TextToSpeech | None = None
        session = self.session_manager.session
        self.last_feed_update = session.last_opened

    async def on_mount(self) -> None:
        session = self.session_manager.session
        session.last_opened = datetime.now()
        self.session_manager.save_session(session)
        feeds = self.feed_manager.get_feeds()
        self._update_feeds_list(feeds)
        self._refresh_feeds()

    def compose(self) -> ComposeResult:
        yield Header()
        yield FeedsList(feed_items=[], id='sidebar-feeds', classes='sidebar-expanded')
        yield ArticlesList(*[], id='sidebar-articles', classes='sidebar-collapsed')
        yield ArticleView()
        yield Footer()

    @on(OptionList.OptionSelected)
    async def option_selected(self, option: OptionList.OptionSelected):
        if option.option_list is self.feeds_option_list:
            if option.option_index < len(self._service_feed_rows()):
                articles_screen = LatestArticlesScreen()
                await self.app.push_screen(articles_screen)
            else:
                # adjusts for the added hardcoded rows in the beginning of the list
                selected_index = option.option_index - len(self._service_feed_rows())
                self.selected_feed = self.feed_manager.get_feeds()[selected_index]
                await self.refresh_selected_feed()
        if isinstance(option.option_list, ArticlesList):
            self.selected_entry = self.selected_feed.entries[option.option_index]
            self._extract_article(self.selected_entry)
            self.selected_entry.meta.is_read = True
            self.feed_manager.save_feeds()
            articles_list_view = self.query_exactly_one(selector=f'#sidebar-articles', expect_type=ArticlesList)
            articles_list_view.replace_option_prompt_at_index(option.option_index,
                                                              Text(self.selected_entry.title, style='italic'))

    def action_open_in_browser(self):
        if self.selected_entry:
            webbrowser.open(self.selected_entry.link)

    async def action_translate_article(self):
        if self.selected_entry:
            self.notify("Translating article. Please wait...")
            self._translate_article()

    async def action_summarize_article(self):
        if self.selected_entry:
            self.notify("Summarizing. Please wait...")
            self._summarize_article()

    async def action_refresh_feeds(self):
        self.selected_feed = self.feed_manager.refresh_feed(self.selected_feed)
        await self.refresh_selected_feed()

    async def action_export_feeds(self):
        feeds = self.feed_manager.get_feeds()
        await self.app.push_screen(
            ConfigFileScreen(
                ConfigFileView(
                    title="Feeds",
                    text=generate_opml(feeds),
                    language="xml"
                )
            )
        )

    async def action_speak_article(self):
        if self.tts and self.tts.is_playing():
            self.tts.cancel()
        else:
            if self.selected_article:
                self.tts = speak_text(self.selected_article.text)
        self.refresh_bindings()

    async def action_pause(self):
        if self.tts:
            self.tts.pause()
            self.refresh_bindings()

    async def action_resume(self):
        if self.tts:
            self.tts.resume()
            self.refresh_bindings()

    def check_action(
            self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:
        actions_while_tts = ['pause']
        actions_while_reading = list(
            map(lambda m: m[1],
                filter(lambda b: b[1] not in actions_while_tts, self.BINDINGS))
        )
        if action == 'resume':
            return self.tts is not None and self.tts.is_paused()
        if action == 'speak_article':
            return has_tts_setup()
        if self.tts and self.tts.is_playing():
            return action in actions_while_reading + actions_while_tts
        else:
            return action in actions_while_reading

    @work(exclusive=True, exit_on_error=False, name='refresh_feeds', thread=True)
    async def _refresh_feeds(self) -> list[Feed]:
        return self.feed_manager.refresh_feeds()

    @work(exclusive=True, exit_on_error=False)
    async def _translate_article(self):
        translator = ArticleTranslator(self.config.language)
        version = await self.feed_manager.create_article_version(self.selected_entry, translator)
        self.selected_article = version.article
        self.update_article_screen(version.article)

    @work(exclusive=True, exit_on_error=False)
    async def _summarize_article(self):
        summarizer = ArticleSummary(self.config.summarization_target_length)
        version = await self.feed_manager.create_article_version(self.selected_entry, summarizer)
        self.selected_article = version.article
        self.update_article_screen(version.article)

    @work(exclusive=True, exit_on_error=False, name='extract_article', thread=True)
    async def _extract_article(self, feed_entry: FeedEntry):
        self.selected_article = self.feed_manager.extract_article(feed_entry)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state == WorkerState.ERROR:
            self.notify(
                title=self._error_title_for_worker(event.worker),
                message=f"Error: {str(event.worker.error)[:300]}",
                severity="error")
            self.log(event)
        if event.worker.name == 'refresh_feeds' and event.state == WorkerState.SUCCESS:
            feeds = event.worker.result
            self._update_feeds_list(feeds)
        if event.worker.name == 'extract_article':
            self._handle_extract_article_update(event)

    def _article_screen(self) -> ArticleView | None:
        return self.query_one(ArticleView)

    def _update_feeds_list(self, feeds: list[Feed]):
        feed_titles = self._service_feed_rows()
        # add a separator in-between
        feed_titles.append(None)
        for feed in feeds:
            feed_titles.append(feed.title)
            feed_titles.append(None)
        self.feeds_option_list.clear_options()
        self.feeds_option_list.add_options(feed_titles)

    @staticmethod
    def _service_feed_rows() -> list:
        """
        There are rows added to the feeds options list that are not actually feeds, but hardcoded
        rows from the application itself. For instance, the "New articles" section - an app generated
        feed with new articles since the app was last opened
        :return: a list of Options - objects that can be added as cells in a OptionList
        """
        last_updated = Table('New articles', expand=True, title_justify='center', caption_justify='center')
        last_updated.add_row('Since you were last here')
        return [last_updated]

    def update_article_screen(self, article: Article):
        screen = self._article_screen()
        screen.selected_entry = self.selected_entry
        screen.selected_article = self.selected_article
        screen.title = article.title
        screen.text = article.text
        screen.update_text()

    async def refresh_selected_feed(self):
        articles_list = self.query_one(ArticlesList)
        articles_list.clear_options()
        articles_list.add_options(self._options_for_feed(self.selected_feed))
        self._restore_selection()

    @property
    def feeds_option_list(self) -> OptionList:
        return self.query_exactly_one(selector=f'#{FeedsList.OPTIONS_LIST_ID}', expect_type=OptionList)

    @staticmethod
    def _options_for_feed(feed: Feed) -> list[Option | None]:
        """
        Returns the options to be added to the FeedsList, sorted chronologically
        :param feed: the selected Feed whose articles will be listed
        :return: a list of options, split by separators, ready to be displayed by an OptionsList
        """
        options = []
        for entry in feed.entries:
            style = 'italic' if hasattr(entry, 'meta') and entry.meta.is_read else 'bold'
            options.append(Option(Text(entry.title, style=style)))
            options.append(None)
        return options

    def _restore_selection(self):
        try:
            index = self.selected_feed.entries.index(self.selected_entry)
            article_list: ArticlesList = cast(ArticlesList, self.query_one(ArticleView))
            article_list.highlighted = index
        except ValueError:
            pass

    @staticmethod
    def _error_title_for_worker(worker: Worker) -> str | None:
        titles_dict = {
            '_translate_article': "Translation failed",
            '_summarize_article': "Summarization failed",
        }
        return titles_dict[worker.name] if worker.name in titles_dict else None

    def _handle_extract_article_update(self, event: Worker.StateChanged):
        if event.state == WorkerState.RUNNING:
            self._article_screen().toggle_loading(True)
        elif event.state == WorkerState.SUCCESS:
            self.update_article_screen(self.selected_article)
            self._article_screen().toggle_loading(False)
        elif event.state == WorkerState.ERROR:
            self._article_screen().toggle_loading(False)
