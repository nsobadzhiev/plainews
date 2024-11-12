from textual.app import ComposeResult
from textual.screen import Screen
from textual.events import Key

from model.article import Article
from ui.article_view import ArticleView


class ArticleScreen(Screen):

    def __init__(
            self,
            article: Article,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        super().__init__(name, id, classes)
        self.article = article

    def compose(self) -> ComposeResult:
        article_view = ArticleView(self.article.text, self.article.title)
        yield article_view

    def on_key(self, event: Key) -> None:
        if event.key == 'q' or event.key == 'escape':
            self.app.pop_screen()
