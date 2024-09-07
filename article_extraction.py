import logging
import sys

from newspaper import Article as NewspaperArticle

from article_presentation import present_article
from model.article import Article

logger = logging.getLogger(__name__)

def extract_article(article_url: str) -> Article:
    article = NewspaperArticle(article_url)
    article.download()
    article.parse()
    article.nlp()
    logger.info(f'Downloaded article: {article.title}')
    return _parse_article(article_url, article)


def _parse_article(article_url: str, news_article: NewspaperArticle) -> Article:
    return Article(
        title=news_article.title,
        text=news_article.text,
        keywords=news_article.keywords,
        image_url=news_article.top_image,
        video_url=news_article.movies[0] if len(news_article.movies) > 0 else None,
        url=article_url,
        language=news_article.meta_lang,
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        style="%",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )
    url = sys.argv[1]
    result = extract_article(url)
    logger.info(result)
    logger.info(result.keywords)
    present_article(result)
