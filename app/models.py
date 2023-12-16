from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(String, primary_key=True, index=True)
    question_id = Column(String, ForeignKey("questions.id"))
    stdout = Column(String)
    time = Column(Float)
    memory = Column(Integer)
    stderr = Column(String, nullable=True)
    token = Column(String)
    compile_output = Column(String, nullable=True)
    message = Column(String, nullable=True)
    status_id = Column(Integer)
    status_description = Column(String)
    created_at = Column(DateTime)
    finished_at = Column(DateTime)


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    tags = Column(String)
