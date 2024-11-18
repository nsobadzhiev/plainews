from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import OptionList, Button

from ui.latest_articles_screen import LatestArticlesScreen


class FeedsList(Widget):

    CSS_PATH = ['feeds_list.tcss']
    OPTIONS_LIST_ID = 'feeds_option_list'

    def __init__(
            self,
            *children: Widget,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
            feed_items: list[str] | None = None,
    ):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self._feed_items = feed_items

    def compose(self) -> ComposeResult:
        yield OptionList(*self._feed_items, id=self.OPTIONS_LIST_ID)
        yield Button('Since you were last here', id='latest_button')

    @on(Button.Pressed, selector='#latest_button')
    def on_latest_articles_pressed(self, button: Button):
        articles_screen = LatestArticlesScreen()
        self.app.push_screen(articles_screen)

    @property
    def feed_items(self) -> list[str]:
        return self._feed_items

    @feed_items.setter
    def feed_items(self, new_value: list[str]):
        self._feed_items = new_value
        self._options_list().clear_options()
        self._options_list().add_options(new_value)

    def _options_list(self) -> OptionList:
        return self.query_exactly_one(selector=f'#{FeedsList.OPTIONS_LIST_ID}', expect_type=OptionList)
