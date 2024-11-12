from datetime import datetime

from model.session import Session
from storage.stored_session import StoredSession


class SessionManager:

    stored_session = StoredSession()

    def __init__(self):
        self.session = self.stored_session.load_session()
        self.session = self.session if self.session else self._empty_session()

    def save_session(self, session: Session | None = None):
        """
        Persistently stores sessions
        :param session: session DTO - if None, the pre-cached object is saved
        :return:
        """
        self.stored_session.save_session(session)

    def update_last_feed_refresh(self, last_refresh: datetime):
        """
        Updates the timestamp of the last feed refresh
        :param last_refresh: datetime when the feeds were last updated
        """
        self.session = self.stored_session.load_session()
        self.session.last_feed_refresh = last_refresh
        self.save_session(self.session)

    @staticmethod
    def _empty_session() -> Session:
        return Session()
