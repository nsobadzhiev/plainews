from datetime import datetime

from pydantic import BaseModel

from model.article_version import ArticleVersion


class FeedEntryMeta(BaseModel):
    """
    Contains metadata attached not from the RSS feed, but from the app.
    For instance, if the entry has been read, a possible generated Article
    object from it etc.
    """
    is_read: bool = False
    base_article: ArticleVersion | None = None
    generated_articles: list[ArticleVersion] = []

    def add_article_version(self, version: ArticleVersion):
        to_replace: ArticleVersion | None = None
        for generated_version in self.generated_articles:
            if isinstance(generated_version, version.__class__):
                to_replace = generated_version
        if to_replace:
            self.generated_articles.remove(to_replace)
        self.generated_articles.append(version)


class FeedEntry(BaseModel):
    entry_id: str
    title: str
    link: str
    publish_date: datetime
    update_date: datetime
    summary: str

    meta: FeedEntryMeta = FeedEntryMeta()

    def __hash__(self):
        return hash(self.entry_id)

    def __eq__(self, other):
        if not isinstance(other, FeedEntry):
            return NotImplemented
        return self.entry_id == other.entry_id

class Feed(BaseModel):
    url: str
    title: str | None
    subtitle: str | None
    entries: list[FeedEntry]
