from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, index=True, primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(TIMESTAMP)
    local_created_at = Column(TIMESTAMP, default=datetime.now)

    def __str__(self) -> str:
        return "Question(id='{}', text='{}', answer='{}', created_at='{}')".format(
            self.id, self.answer, self.answer, self.created_at
        )
