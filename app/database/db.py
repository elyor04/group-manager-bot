from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..utils.config import DB_PATH
from .models import Base

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
session = Session(bind=engine)


def initialize_db():
    Base.metadata.create_all(engine)


def close_db():
    session.close()
