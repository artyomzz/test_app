import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.types import BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, default=uuid.uuid4(), index=True, primary_key=True)
    access_token = Column(UUID, default=uuid.uuid4(), unique=True)
    username = Column(String(128), unique=True)

    def __str__(self) -> str:
        return f"User(id='{self.id}', username='{self.username}')"


class Record(Base):
    __tablename__ = "records"

    id = Column(UUID, default=uuid.uuid4(), index=True, primary_key=True)
    data = Column(BYTEA)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    access_token = Column(UUID, ForeignKey("users.access_token", ondelete="CASCADE"))

    def __str__(self) -> str:
        return f"Record(id='{self.id}', user_id='{self.user_id}')"
