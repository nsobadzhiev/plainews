import logging

from newspaper import Article as NewspaperArticle

from model.article import Article

logger = logging.getLogger(__name__)

def extract_article(article_url: str) -> Article:
    article = NewspaperArticle(article_url)
    article.download()
    try:
        return _parse_article(article_url, article)
    except LookupError:
        # Newspaper needs some tokenizers from nltk.
        # Download them and try again
        import nltk
        nltk.download('punkt_tab')
        return _parse_article(article_url, article)


def _parse_article(article_url: str, news_article: NewspaperArticle) -> Article:
    news_article.parse()
    news_article.nlp()
    return Article(
        title=news_article.title,
        text=news_article.text,
        keywords=news_article.keywords,
        image_url=news_article.top_image,
        video_url=news_article.movies[0] if len(news_article.movies) > 0 else None,
        url=article_url,
        language=news_article.meta_lang,
    )
