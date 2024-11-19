from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


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
