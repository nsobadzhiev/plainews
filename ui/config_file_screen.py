from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen

from ui.config_file_view import ConfigFileView


class ConfigFileScreen(ModalScreen):
    CSS_PATH = ['config_file_view.tcss']

    def __init__(
            self,
            file_view: ConfigFileView,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        super().__init__(name, id, classes)
        self.file_view = file_view

    def compose(self) -> ComposeResult:
        yield self.file_view

    @on(ConfigFileView.Escape)
    def on_pop_screen(self):
        self.app.pop_screen()
