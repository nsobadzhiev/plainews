from datetime import datetime

from pydantic import BaseModel


class FeedEntry(BaseModel):
    entry_id: str
    title: str
    link: str
    publish_date: datetime
    update_date: datetime
    summary: str

class Feed(BaseModel):
    url: str
    title: str
    subtitle: str
    entries: list[FeedEntry]
