from datetime import datetime, timedelta
from typing import cast

from textual import events, work
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import SelectionList, Label, Button
from textual.worker import Worker, WorkerState

from model.article import Article
from model.feed import FeedEntry
from model.feed_manager import FeedManager
from model.latest_articles import articles_since, articles_summary
from model.session_manager import SessionManager
from ui.article_screen import ArticleScreen


class LatestArticlesView(Widget):

    class Escape(Message):
        pass

    session_manager = SessionManager()
    feed_manager = FeedManager()

    def __init__(self,
                 *children: Widget,
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None,
                 disabled: bool = False,
                 ):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.current_items: list[FeedEntry] = []

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('What happened since you were last here:', id='latest_articles_title'),
            SelectionList[int](*[], id='latest_articles_list'),
            Button("Create a summary", variant="primary", id="summary_button"),
            Button("Open selected article", variant="default", id="open_button"),
            id='latest_articles_grid',
        )

    async def on_mount(self, event: events.Mount) -> None:
        self.latest_articles_list.loading = True
        self.load_articles()

    def on_key(self, event: Key) -> None:
        if event.key == 'q' or event.key == 'escape':
            self.post_message(self.Escape())

    @property
    def latest_articles_list(self) -> SelectionList:
        return self.query_exactly_one(SelectionList)

    @property
    def create_summary_button(self) -> Button:
        return self.query_exactly_one(selector='#summary_button', expect_type=Button)

    @on(Button.Pressed, '#summary_button')
    async def on_create_summary(self):
        self.create_summary()

    @on(Button.Pressed, '#open_button')
    async def on_open_article(self):
        selected_item_index = self.latest_articles_list.highlighted
        if selected_item_index:
            feed_entry: FeedEntry = self.current_items[cast(int, selected_item_index)]
            article = feed_entry.meta.base_article if feed_entry.meta.base_article \
                else self.feed_manager.extract_article(feed_entry)
            await self.app.push_screen(ArticleScreen(feed_entry, article))

    @work(exclusive=True, name="load_articles", exit_on_error=False, thread=True)
    async def load_articles(self):
        self.current_items = articles_since(
            self._last_opened_time() - timedelta(days=1), force_fetch=False
        )

    @work(exclusive=True, exit_on_error=False)
    async def create_summary(self) -> Article:
        self.create_summary_button.loading = True
        selected_item_indexes = self.latest_articles_list.selected
        selected_entries = [self.current_items[index] for index in selected_item_indexes]
        return await articles_summary(selected_entries)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        # only the worker completed and failed events are interesting
        if event.state == WorkerState.ERROR:
            self.notify(
                title="Failed to generate latest articles summary",
                message=f"Error: {str(event.worker.error)[:300]}",
                severity="error")
            self.log(event)
            self.latest_articles_list.loading = False
            self.create_summary_button.loading = False
        elif event.state == WorkerState.SUCCESS:
            if event.worker.name == 'create_summary':
                result = event.worker.result
                self.app.push_screen(ArticleScreen(article=result))
                self.create_summary_button.loading = False
            if event.worker.name == 'load_articles':
                self._update_titles()

    @staticmethod
    def _selection_list_items(titles: list[str]) -> list[tuple[str, int, bool]]:
        return [(title, index, False) for index, title in enumerate(titles)]

    def _last_opened_time(self) -> datetime:
        # it's important to NOT return the min date here because then
        # generating a date that's prior to the min one, throws an exception
        # Default to ~ year ago
        return self.session_manager.session.last_opened \
            if self.session_manager.session.last_feed_refresh \
            else datetime.now() - timedelta(weeks=54)

    def _update_titles(self):
        titles = [entry.title for entry in self.current_items]
        self.latest_articles_list.clear_options()
        self.latest_articles_list.add_options(self._selection_list_items(titles))
        self.latest_articles_list.loading = False
