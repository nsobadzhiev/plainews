from textual.app import ComposeResult
from textual.events import Key
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import TextArea, Static
from textual.message import Message

class ConfigFileView(Widget):

    title = reactive("Configuration file")
    text = reactive('Select an item on the left')
    code_language = 'yaml'

    class Escape(Message):
        pass

    def __init__(
            self,
            title: str,
            text: str,
            language: str,
            id: str | None = None,
    ):
        super().__init__(id=id)
        self.text = text
        self.title = title
        self.code_language = language

    def compose(self) -> ComposeResult:
        yield Static(self.title, id='article-title')
        yield TextArea(self.text, id='article-text').code_editor(
            read_only=True,
            show_line_numbers=True,
            language=self.code_language,
            text=self.text,
        )

    def on_key(self, event: Key) -> None:
        if event.key == 'q' or event.key == 'escape':
            self.post_message(self.Escape())
