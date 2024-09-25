from datetime import datetime

from pydantic import BaseModel


class FeedEntry(BaseModel):
    entry_id: str
    title: str
    link: str
    publish_date: datetime
    update_date: datetime
    summary: str

    def __hash__(self):
        return hash(self.entry_id)

    def __eq__(self, other):
        if not isinstance(other, FeedEntry):
            return NotImplemented
        return self.entry_id == other.entry_id

class Feed(BaseModel):
    url: str
    title: str
    subtitle: str | None
    entries: list[FeedEntry]
