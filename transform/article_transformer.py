from model.article import Article
from model.article_version import ArticleVersion


class ArticleTransformer:

    async def transformed_article(self, article: Article) -> ArticleVersion:
        """
        Performs a transformation of the article - it post-processes the input
        and brings a more refined version (in a different language, just a summary etc.)
        :param article: the raw article
        :return: a new ArticleVersion object that has the target transformation applied to it
        """
        pass
