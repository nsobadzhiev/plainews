from ai.llm_translate import translate_text
from model.article import Article
from transform.article_transformer import ArticleTransformer


class ArticleTranslator(ArticleTransformer):

    def __init__(self, target_language: str):
        self.target_language = target_language

    def transformed_article(self, article: Article) -> Article:
        """
        Returns the same contents in a different language (target_language)
        """
        translated_article: Article = article.copy()
        translated_article.text = translate_text(article.text, self.target_language)
        return translated_article
