from model.feed_manager import FeedManager


def test_storing_feed():
    feed_manager = FeedManager()
    feed_manager.add_feed("https://rss.sueddeutsche.de/rss/Topthemen")
    feeds = feed_manager.get_feeds()
    assert len(feeds) == 1
