from ai.llm_translate import translate_text
from model.article import Article
from model.article_version import ArticleVersion, TranslatedArticle
from transform.article_transformer import ArticleTransformer


class ArticleTranslator(ArticleTransformer):

    def __init__(self, target_language: str):
        self.target_language = target_language

    async def transformed_article(self, article: Article) -> ArticleVersion:
        """
        Returns the same contents in a different language (target_language)
        """
        translated_article: Article = article.model_copy()
        translated_article.text = await translate_text(article.text, self.target_language)
        return TranslatedArticle(
            language=self.target_language,
            article=translated_article,
            parent_article=article,
        )
