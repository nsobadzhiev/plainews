from pydantic import BaseModel

from model.article import Article


class ArticleVersion(BaseModel):
    """
    An extension to the Article class that adds metadata regarding the
    reason for, and the options with which an article was generated.
    For instance, it's a translation of a source article, or it was a summary
    """
    parent_article: Article | None = None
    article: Article | None = None


class TranslatedArticle(ArticleVersion):
    language: str


class SummarizedArticle(ArticleVersion):
    target_word_length: int
