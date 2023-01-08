from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.db.session import get_session


class BaseService:
    def __init__(self, session: sessionmaker = Depends(get_session)):
        self.async_session = session
