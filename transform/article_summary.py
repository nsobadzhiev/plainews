from ai.llm_summarize import summarize_text
from model.article import Article
from model.article_version import ArticleVersion, SummarizedArticle
from transform.article_transformer import ArticleTransformer


class ArticleSummary(ArticleTransformer):

    def __init__(self, target_length: int):
        self.target_length = target_length

    async def transformed_article(self, article: Article) -> ArticleVersion:
        """
        Returns a more concise version of the source article
        """
        short_article = article.model_copy()
        short_article.text = await summarize_text(article.text, self.target_length)
        return SummarizedArticle(
            parent_article=article,
            article=short_article,
            target_word_length=self.target_length,
        )
