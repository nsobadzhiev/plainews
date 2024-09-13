from model.article import Article
from transform.article_transformer import ArticleTransformer


class ArticleSummary(ArticleTransformer):

    async def transformed_article(self, article: Article) -> Article:
        """
        Returns a more concise version of the source article
        """
        return article
