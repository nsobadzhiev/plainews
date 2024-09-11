import sys
from datetime import datetime
from time import mktime

import feedparser

from model.feed import Feed, FeedEntry


def parse_rss_feed(feed_url: str) -> Feed:
    rss = feedparser.parse(feed_url)
    title = rss.feed.title
    subtitle = rss.feed.subtitle if 'subtitle' in rss.feed else None
    entries = []
    for entry in rss.entries:
        entry_title = entry.title
        entry_link = entry.link
        entry_id = entry.id
        publish_date = datetime.fromtimestamp(mktime(entry.published_parsed))
        update_date = datetime.fromtimestamp(mktime(entry.updated_parsed))
        summary = entry.summary
        feed_entry = FeedEntry(
            entry_id=entry_id,
            title=entry_title,
            link=entry_link,
            summary=summary,
            publish_date=publish_date,
            update_date=update_date
        )
        entries.append(feed_entry)
    return Feed(
        title=title,
        subtitle=subtitle,
        entries=entries,
        url=feed_url,
    )


if __name__ == "__main__":
    rss_url = sys.argv[1]
    feed = parse_rss_feed(rss_url)
    print(f"Parsed feed: {feed}")
