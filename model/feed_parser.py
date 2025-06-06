import sys
from datetime import datetime
from time import mktime

import feedparser

from model.feed import Feed, FeedEntry


def parse_rss_feed(feed_url: str) -> Feed:
    rss = feedparser.parse(feed_url)
    title = rss.feed.title if 'title' in rss.feed else None
    subtitle = rss.feed.subtitle if 'subtitle' in rss.feed else None
    entries = []
    for entry in rss.entries:
        entry_title = entry.title
        entry_link = entry.link
        entry_id = entry.id if 'id' in entry else entry.link
        publish_date = datetime.fromtimestamp(mktime(entry.published_parsed)) if 'published_parsed' in entry else None
        update_date = datetime.fromtimestamp(mktime(entry.updated_parsed)) if 'updated_parsed' in entry else None
        summary = entry.summary if 'summary' in entry else ''
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
        entries=sorted(entries, key=lambda e: (e.update_date is None, e.update_date), reverse=True),
        url=feed_url,
    )


if __name__ == "__main__":
    rss_url = sys.argv[1]
    feed = parse_rss_feed(rss_url)
    print(f"Parsed feed: {feed}")
