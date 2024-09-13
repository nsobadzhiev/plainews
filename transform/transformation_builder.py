from config.config import Config
from model.article import Article
from transform.article_summary import ArticleSummary
from transform.article_transformer import ArticleTransformer
from transform.article_translator import ArticleTranslator


class TransformationBuilder:

    config = Config()
    transformer_mapping = {
        "ArticleTranslator": ArticleTranslator(config.language),
        "ArticleSummary": ArticleSummary()
    }

    def __init__(self, transformers: list[ArticleTransformer]):
        self.transformers = transformers

    async def transform(self, article: Article) -> Article:
        result = article
        for transformer in self.transformers:
            result = transformer.transformed_article(result)
        return result

    @staticmethod
    def from_names(transformer_names: list[str]) -> "TransformationBuilder":
        return TransformationBuilder(
            list(map(lambda name: TransformationBuilder.transformer_mapping[name], transformer_names))
        )

    @staticmethod
    def from_config() -> "TransformationBuilder":
        return TransformationBuilder(
            list(map(
                lambda name: TransformationBuilder.transformer_mapping[name],
                TransformationBuilder.config.transformers)
            )
        )
