import os
import pickle
from config.config import Config
from model.feed import Feed
from storage.config_dir import create_config_dir


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

    def get_feed(self, url: str) -> Feed | None:
        for feed in self.feeds:
            if feed.url == url:
                return feed
        return None

    def merge_feed(self, feed: Feed) -> Feed:
        """
        Adds the feed to the storage. If the feed already exists, merges the
        already stored entries with any new ones from the `feed` parameter. Stores the
        merged entries in chronological order
        :param feed: the feed to merge into the storage
        :return: the (possibly modified) feed that was stored
        """
        existing_feed = self.get_feed(feed.url)
        if not existing_feed:
            self.add_feed(feed)
            return feed
        else:
            merged = self._merged_feed(existing_feed, feed)
            self.replace_feed(existing_feed, merged)
            return merged

    def replace_feed(self, old_feed: Feed, new_feed: Feed):
        """
        As opposed to removing and adding a feed, this method keeps the
        order in the feed list
        """
        self.feeds = [feed if feed.url != old_feed.url else new_feed for feed in self.feeds]
        self.save_feeds()

    def save_feeds(self):
        try:
            with open(self.config.feeds_file, 'wb') as storage_file:
                pickle.dump(self.feeds, storage_file)
        except FileNotFoundError:
            if create_config_dir():
                # retry (caution - it's recursing)
                self.save_feeds()

    def load_feeds(self):
        if os.path.exists(self.config.feeds_file):
            with open(self.config.feeds_file, 'rb') as feeds_file:
                self.feeds = pickle.load(feeds_file)

    @staticmethod
    def _merged_feed(existing_feed: Feed, new_feed: Feed) -> Feed:
        merged_set = set(existing_feed.entries)
        merged_set.update(new_feed.entries)
        return Feed(
            entries=sorted(list(merged_set), key=lambda e: (e.update_date is None, e.update_date), reverse=True),
            url=new_feed.url,
            title=new_feed.title,
            subtitle=new_feed.subtitle,
        )
