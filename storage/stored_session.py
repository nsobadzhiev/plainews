import os
import pickle

from config.config import Config
from model.session import Session


class StoredSession:

    config = Config()

    def __init__(self):
        self.session: Session | None = None
        self.load_session()

    def save_session(self, new_session: Session):
        self.session = new_session
        with open(self.config.session_file, 'wb') as session_file:
            pickle.dump(self.session, session_file)

    def load_session(self) -> Session | None:
        if os.path.exists(self.config.session_file):
            with open(self.config.session_file, 'rb') as session_file:
                self.session = pickle.load(session_file)
                return self.session
        return None
