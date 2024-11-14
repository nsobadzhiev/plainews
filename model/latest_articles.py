import functools
from datetime import datetime

from model.article import Article
from model.feed import FeedEntry
from model.feed_manager import FeedManager
from model.feed_pipeline import FeedPipeline
from transform.article_summary import ArticleSummary


def articles_since(since_date: datetime, force_fetch: bool) -> list[FeedEntry]:
    feed_manager = FeedManager()
    if force_fetch or feed_manager.outdated_feeds():
        feed_manager.refresh_feeds()
        feed_manager.session_manager.update_last_feed_refresh(datetime.now())
    feeds = feed_manager.get_feeds()
    entries = functools.reduce(lambda a, b: a + b.entries, feeds, [])
    return list(filter(lambda e: since_date < e.publish_date, entries))


async def latest_articles_summary(since_date: datetime, force_fetch: bool) -> Article:
    entries = articles_since(since_date, force_fetch)
    return await articles_summary(entries)


async def articles_summary(entries: list[FeedEntry], delimiter: str = '\n\n-------------\n\n') -> Article:
    pipeline = _latest_articles_pipeline(entries)
    articles = await pipeline.transform()
    article_texts = [article.text for article in articles]
    summary = delimiter.join(article_texts)
    return Article(
        title=f"Summary of the selected articles",
        text=summary,
        language='english',
        url='',
        keywords=[],
        video_url=None,
        image_url=None,
    )


def _latest_articles_pipeline(entries: list[FeedEntry]) -> FeedPipeline:
    return FeedPipeline(entries, transformers=[
        ArticleSummary(150)
    ])
