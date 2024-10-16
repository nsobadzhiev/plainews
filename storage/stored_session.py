import os
import pickle

from config.config import Config
from model.session import Session
from storage.config_dir import create_config_dir


class StoredSession:

    config = Config()

    def __init__(self):
        self.session: Session | None = None
        self.load_session()

    def save_session(self, new_session: Session):
        self.session = new_session
        try:
            with open(self.config.session_file, 'wb') as session_file:
                pickle.dump(self.session, session_file)
        except FileNotFoundError:
            if create_config_dir():
                # retry (caution - it's recursing)
                self.save_session(new_session)

    def load_session(self) -> Session | None:
        if os.path.exists(self.config.session_file):
            with open(self.config.session_file, 'rb') as session_file:
                self.session = pickle.load(session_file)
                return self.session
        return None
