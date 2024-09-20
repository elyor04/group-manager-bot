from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
session = sessionmaker(bind=engine)()
Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"

    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    warnings = Column(Integer, default=0)
    muted = Column(Integer, default=0)
    banned = Column(Integer, default=0)
    messages = Column(Integer, default=0)

    def __repr__(self):
        return f"<UserInfo(chat_id={self.chat_id}, user_id={self.user_id})>"


def initialize_db():
    Base.metadata.create_all(engine)


def close_db():
    session.close()
