from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import TextArea, Static


class ArticleScreen(Widget):

    title = reactive("No article selected")
    text = reactive('Select an item on the left')

    def __init__(self, text: str, id: str | None = None):
        super().__init__(id=id)
        self.text = text

    def update_text(self):
        title = self.query_one(Static)
        title.update(self.title)
        body = self.query_one(TextArea)
        body.text = self.text

    def compose(self) -> ComposeResult:
        yield Static(self.title, id='article-title')
        area = TextArea(self.text, id='article-text')
        area.read_only = True
        yield area
