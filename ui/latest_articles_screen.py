from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen

from ui.latest_articles_view import LatestArticlesView


class LatestArticlesScreen(ModalScreen):

    CSS_PATH = ['latest_articles_view.tcss']

    def compose(self) -> ComposeResult:
        yield LatestArticlesView()

    @on(LatestArticlesView.Escape)
    def on_pop_screen(self):
        self.app.pop_screen()
