from model.article import Article


class ArticleTransformer:

    async def transformed_article(self, article: Article) -> Article:
        """
        Performs a transformation of the article - it post-processes the input
        and brings a more refined version (in a different language, just a summary etc.)
        :param article: the raw article
        :return: a new Article object that has the target transformation applied to it
        """
        pass
