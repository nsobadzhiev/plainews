from model.article import Article
from model.feed import FeedEntry
from model.feed_manager import FeedManager
from transform.article_transformer import ArticleTransformer


class FeedPipeline:

    feed_manager = FeedManager()

    def __init__(self, entries: list[FeedEntry], transformers: list[ArticleTransformer]):
        self.entries = entries
        self.transformers = transformers

    async def transform(self) -> list[Article]:
        articles = [self.feed_manager.extract_article(entry) for entry in self.entries]
        transformed = [await self._apply_transformations(article) for article in articles]
        return transformed

    async def _apply_transformations(self, article: Article) -> Article:
        transformed_article = article
        for trans in self.transformers:
            new_version = await trans.transformed_article(transformed_article)
            transformed_article = new_version.article
        return transformed_article
