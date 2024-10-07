from datetime import datetime

from pydantic import BaseModel

class Session(BaseModel):
    """
    Contains app sessions - not to be confused with the app config
    that's stored as a yaml configuration file. A session contains
    state variables that the application generates and stores.
    """
    last_opened: datetime | None = None
