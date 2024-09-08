import logging
from typing import cast

from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.widgets.option_list import Option
from textual.widgets.option_list import Separator

from article_extraction import extract_article
from config.config import Config
from model.article import Article
from model.feed import Feed
from model.feed_manager import FeedManager
from ui.article_screen import ArticleScreen
from ui.articles_list import ArticlesList
from ui.feeds_list import FeedsList

logger = logging.getLogger(__name__)


class HomeScreen(Screen[None]):

    CSS_PATH = ['home_layout.tcss', 'article_layout.tcss']

    config = Config()
    feed_manager = FeedManager()

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.plainews = cast("Plainews", self.app)
        self.selected_feed: Feed | None = None
        self.selected_article: Article | None = None

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        feeds = self.feed_manager.get_feeds()
        feed_titles = list(map(lambda f: f.title, feeds))
        yield Header()
        yield FeedsList(*feed_titles, id='sidebar-feeds', classes='sidebar-expanded')
        yield ArticlesList(*[], id='sidebar-articles', classes='sidebar-collapsed')
        yield ArticleScreen("")
        yield Footer()

    @on(FeedsList.OptionSelected)
    async def feed_selected(self, option: FeedsList.OptionSelected):
        if isinstance(option.option_list, FeedsList):
            selected_index = option.option_index
            self.selected_feed = self.feed_manager.get_feeds()[selected_index]
            articles_list = self.query_one(ArticlesList)
            articles_list.clear_options()
            articles_list.add_options(self._options_for_feed(self.selected_feed))
        if isinstance(option.option_list, ArticlesList):
            article_screen = self.query_one(ArticleScreen)
            feed_entry = self.selected_feed.entries[option.option_index]
            self.selected_article = extract_article(feed_entry.link)
            article_screen.title = self.selected_article.title
            article_screen.text = self.selected_article.text
            article_screen.update_text()

    @staticmethod
    def _options_for_feed(feed: Feed) -> list[Option | Separator]:
        """
        Returns the options to be added to the FeedsList, sorted chronologically
        :param feed: the selected Feed whose articles will be listed
        :return: a list of options, split by separators, ready to be displayed by an OptionsList
        """
        latest_entries = sorted(feed.entries, key=lambda e: e.update_date, reverse=True)
        options = []
        for entry in latest_entries:
            options.append(entry.title)
            options.append(Separator())
        return options

    # @on(ScreenResume)
    # async def reload_screen(self) -> None:
    #     articles_list = self.query_one(ArticlesList)
    #     stored = StoredFeeds([]).load_feeds()
    #     articles_list = stored.feeds[0].articles if len(stored.feeds) > 0 else []
    #     await articles_list.reload_and_refresh()

    # @on(ChatList.ChatOpened)
    # async def open_chat_screen(self, event: ChatList.ChatOpened):
    #     chat_id = event.chat.id
    #     assert chat_id is not None
    #     chat = await self.chats_manager.get_chat(chat_id)
    #     await self.app.push_screen(ChatScreen(chat))

    # @on(ChatList.CursorEscapingTop)
    # def cursor_escaping_top(self):
    #     self.query_one(HomePromptInput).focus()

    # @on(PromptInput.PromptSubmitted)
    # async def create_new_chat(self, event: PromptInput.PromptSubmitted) -> None:
    #     text = event.text
    #     await self.elia.launch_chat(  # type: ignore
    #         prompt=text,
    #         model=self.elia.runtime_config.selected_model,
    #     )

    # @on(PromptInput.CursorEscapingBottom)
    # async def move_focus_below(self) -> None:
    #     self.focus_next(ChatList)
    #
    # async def action_options(self) -> None:
    #     await self.app.push_screen(
    #         OptionsModal(),
    #         callback=self.update_config,
    #     )
