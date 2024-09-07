import os
import pickle
from config.config import Config
from model.feed import Feed


class StoredFeeds:

    config = Config()

    def __init__(self, feeds: list[Feed]):
        self.feeds = feeds

    def add_feed(self, feed: Feed):
        self.feeds.append(feed)
        self.save_feeds()

    def set_feeds(self, feeds: list[Feed]):
        self.feeds = feeds
        self.save_feeds()

    def remove_feed(self, feed: Feed):
        self.feeds.remove(feed)
        self.save_feeds()

    def remove_feeds(self):
        self.feeds = []
        self.save_feeds()

    def save_feeds(self):
        with open(self.config.feeds_file, 'wb') as storage_file:
            pickle.dump(self.feeds, storage_file)

    def load_feeds(self):
        if os.path.exists(self.config.feeds_file):
            with open(self.config.feeds_file, 'rb') as feeds_file:
                self.feeds = pickle.load(feeds_file)
