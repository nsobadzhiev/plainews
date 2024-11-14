from textual.app import ComposeResult
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Footer

from model.article import Article
from model.feed import FeedEntry
from ui.article_view import ArticleView


class ArticleScreen(Screen):

    def __init__(
            self,
            feed_entry: FeedEntry | None = None,
            article: Article | None = None,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        super().__init__(name, id, classes)
        self.article = article
        self.feed_entry = feed_entry

    def compose(self) -> ComposeResult:
        article_view = ArticleView(self.feed_entry, self.article)
        yield article_view
        yield Footer()

    def on_key(self, event: Key) -> None:
        if event.key == 'q' or event.key == 'escape':
            self.app.pop_screen()
