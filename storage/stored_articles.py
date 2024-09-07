import pickle

from config.config import Config
from model.article import Article


class StoredArticles:

    config = Config()
    storage_file = open(config.articles_file, 'wb')

    def __init__(self):
        self.articles = dict()

    def add_article(self, article: Article):
        self.articles[article.url] = article
        self.save_articles()

    def article_for_url(self, url: str) -> Article | None:
        return self.articles[url]
        
    def save_articles(self):
        pickle.dump(self.articles, self.storage_file)

    def load_articles(self):
        with open(self.config.articles_file, 'rb') as articles_file:
            self.articles = pickle.load(articles_file)
