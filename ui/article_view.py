import webbrowser

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import TextArea, Static
from textual import work

from ai.tts import speak_text, has_tts_setup, TextToSpeech
from config.config import Config
from model.article import Article
from model.feed import FeedEntry
from model.feed_manager import FeedManager
from transform.article_summary import ArticleSummary
from transform.article_transformer import ArticleTransformer
from transform.article_translator import ArticleTranslator


class ArticleView(Widget):
    BINDINGS = [
        ("o", "open_in_browser", "Open in browser"),
        ("t", "translate_article", "Translate"),
        ("s", "summarize_article", "Summarize"),
        ("a", "speak_article", "Audio"),
        ("p", "pause", "Pause"),
        ("c", "resume", "Resume"),
    ]

    title = reactive("No article selected")
    text = reactive('Select an item on the left')

    config = Config()
    feed_manager = FeedManager()

    def __init__(
            self,
            entry: FeedEntry | None = None,
            selected_article: Article | None = None,
            id: str | None = None
    ):
        super().__init__(id=id)
        self.tts: TextToSpeech | None = None
        self.selected_entry = entry
        base_article = entry.meta.base_article if entry else None
        self.selected_article = selected_article if selected_article else base_article
        self.title = self.selected_article.title if self.selected_article else ""
        self.text = self.selected_article.text if self.selected_article else ""

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

    def action_open_in_browser(self):
        if self.selected_entry:
            webbrowser.open(self.selected_entry.link)

    async def action_translate_article(self):
        self.notify("Translating article. Please wait...")
        self._translate_article()

    async def action_summarize_article(self):
        self.notify("Summarizing. Please wait...")
        self._summarize_article()

    async def action_speak_article(self):
        if self.tts and self.tts.is_playing():
            self.tts.cancel()
        else:
            if self.selected_article:
                self.tts = speak_text(self.selected_article.text)
        self.refresh_bindings()

    async def action_pause(self):
        if self.tts:
            self.tts.pause()
            self.refresh_bindings()

    async def action_resume(self):
        if self.tts:
            self.tts.resume()
            self.refresh_bindings()

    def check_action(
            self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:
        actions_while_tts = ['pause']
        actions_while_reading = list(
            map(lambda m: m[1],
                filter(lambda b: b[1] not in actions_while_tts, self.BINDINGS))
        )
        if action == 'open_in_browser':
            return self.selected_entry is not None and self.selected_entry.link is not None
        if action == 'resume':
            return self.tts is not None and self.tts.is_paused()
        if action == 'speak_article':
            return has_tts_setup()
        if self.tts and self.tts.is_playing():
            return action in actions_while_reading + actions_while_tts
        else:
            return action in actions_while_reading

    @work(exclusive=True, exit_on_error=False)
    async def _translate_article(self):
        translator = ArticleTranslator(self.config.language)
        await self._apply_transformer(translator)

    @work(exclusive=True, exit_on_error=False)
    async def _summarize_article(self):
        summarizer = ArticleSummary(self.config.summarization_target_length)
        await self._apply_transformer(summarizer)

    def _update_view(self, article: Article):
        self.title = article.title
        self.text = article.text
        self.update_text()

    def _toggle_loading(self, is_loading: bool):
        self.query_one(Static).loading = is_loading

    async def _apply_transformer(self, transformer: ArticleTransformer):
        self._toggle_loading(True)
        if self.selected_entry:
            version = await self.feed_manager.create_article_version(self.selected_entry, transformer)
            self.selected_article = version.article
        else:
            new_version = await transformer.transformed_article(self.selected_article)
            self.selected_article = new_version.article
        self._update_view(self.selected_article)
        self._toggle_loading(False)
