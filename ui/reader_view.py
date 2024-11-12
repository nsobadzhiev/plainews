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
from textual.widgets.option_list import Separator
from textual.worker import Worker, WorkerState

from ai.tts import speak_text, TextToSpeech, has_tts_setup
from config.config import Config
from model.article import Article
from model.feed import Feed, FeedEntry
from model.feed_manager import FeedManager
from model.session_manager import SessionManager
from transform.article_summary import ArticleSummary
from transform.article_translator import ArticleTranslator
from rich.text import Text
from ui.article_view import ArticleView
from ui.articles_list import ArticlesList
from ui.feeds_list import FeedsList

logger = logging.getLogger(__name__)


class ReaderView(Widget):

    CSS_PATH = ['reader_view.tcss', 'article_layout.tcss']

    BINDINGS = [
        ("o", "open_in_browser", "Open in browser"),
        ("t", "translate_article", "Translate"),
        ("s", "summarize_article", "Summarize"),
        ("a", "speak_article", "Audio"),
        ("r", "refresh_feeds", "Refresh"),
        ("p", "pause", "Pause"),
        ("c", "resume", "Resume"),
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

    def on_mount(self) -> None:
        session = self.session_manager.session
        session.last_opened = datetime.now()
        self.session_manager.save_session(session)

    def compose(self) -> ComposeResult:
        feeds = self.feed_manager.get_feeds()
        feed_titles = list(map(lambda f: f.title, feeds))
        yield Header()
        yield FeedsList(feed_items=feed_titles, id='sidebar-feeds', classes='sidebar-expanded')
        yield ArticlesList(*[], id='sidebar-articles', classes='sidebar-collapsed')
        yield ArticleView("")
        yield Footer()

    @on(OptionList.OptionSelected)
    async def feed_selected(self, option: OptionList.OptionSelected):
        if option.option_list is self.feeds_option_list:
            selected_index = option.option_index
            self.selected_feed = self.feed_manager.get_feeds()[selected_index]
            await self.refresh_selected_feed()
        if isinstance(option.option_list, ArticlesList):
            self.selected_entry = self.selected_feed.entries[option.option_index]
            self.selected_article = self.feed_manager.extract_article(self.selected_entry)
            self.selected_entry.meta.is_read = True
            self.update_article_screen(self.selected_article)
            self.feed_manager.save_feeds()
            await self.refresh_selected_feed()

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

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state == WorkerState.ERROR:
            self.notify(
                title=self._error_title_for_worker(event.worker),
                message=f"Error: {str(event.worker.error)[:300]}",
                severity="error")
            self.log(event)

    def _article_screen(self) -> ArticleView | None:
        return self.query_one(ArticleView)

    def update_article_screen(self, article: Article):
        screen = self._article_screen()
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
    def _options_for_feed(feed: Feed) -> list[Option | Separator]:
        """
        Returns the options to be added to the FeedsList, sorted chronologically
        :param feed: the selected Feed whose articles will be listed
        :return: a list of options, split by separators, ready to be displayed by an OptionsList
        """
        options = []
        for entry in feed.entries:
            style = 'italic' if hasattr(entry, 'meta') and entry.meta.is_read else 'bold'
            options.append(Text(entry.title, style=style))
            options.append(Separator())
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

