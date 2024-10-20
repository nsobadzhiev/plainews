import logging

from textual.app import ComposeResult
from textual.screen import Screen

from ui.reader_view import ReaderView

logger = logging.getLogger(__name__)


class HomeScreen(Screen[None]):

    CSS_PATH = ['home_layout.tcss', 'reader_view.tcss', 'article_layout.tcss']

    def compose(self) -> ComposeResult:
        yield ReaderView()
