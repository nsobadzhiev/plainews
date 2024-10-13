from config.config import Config
from model.article import Article
from model.article_version import ArticleVersion
from model.feed import Feed, FeedEntry
from storage.stored_feeds import StoredFeeds
from model.feed_parser import parse_rss_feed
from model.article_extraction import extract_article
from transform.article_transformer import ArticleTransformer


def _article_from_feed_entry(feed_entry: FeedEntry) -> Article:
    article = extract_article(feed_entry.link)
    return article


class FeedManager:

    storage = StoredFeeds([])
    config = Config()

    def __init__(self):
        self.refresh_feeds()

    def add_feed(self, feed_url: str) -> Feed:
        feed = parse_rss_feed(feed_url)
        self.storage.add_feed(feed)
        return feed

    def refresh_feed(self, feed: Feed) -> Feed:
        new_feed = parse_rss_feed(feed.url)
        self._replace_feed(feed, new_feed)
        return new_feed

    def refresh_feeds(self) -> list[Feed]:
        feeds = list(map(lambda feed_url: parse_rss_feed(feed_url), self.config.followed_feeds))
        if self.config.history.keep_history:
            self.storage.load_feeds()
            [self.storage.merge_feed(feed) for feed in feeds]
            return self.get_feeds()
        else:
            self.storage.set_feeds(feeds)
        return feeds

    def get_feeds(self) -> list[Feed]:
        return self.storage.feeds

    def remove_feed(self, feed: Feed):
        self.storage.remove_feed(feed)
        self.storage.save_feeds()

    def save_feeds(self):
        self.storage.save_feeds()

    @staticmethod
    def extract_article(feed_entry: FeedEntry) -> Article:
        article = extract_article(feed_entry.link)
        extracted_version = ArticleVersion(
            parent_article=None,
            article=article,
        )
        feed_entry.meta.base_article = article
        feed_entry.meta.add_article_version(extracted_version)
        return article

    async def create_article_version(self, feed_entry: FeedEntry, transformer: ArticleTransformer) -> ArticleVersion:
        base_article = feed_entry.meta.base_article
        if not base_article:
            base_article = self.extract_article(feed_entry)
        transformed = await transformer.transformed_article(base_article)
        feed_entry.meta.add_article_version(transformed)
        self.save_feeds()
        return transformed

    def _replace_feed(self, old_feed: Feed, new_feed: Feed):
        self.storage.replace_feed(old_feed, new_feed)

