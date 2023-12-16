from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

question_tag_association = Table(
    'question_tag_association',
    Base.metadata,
    Column('question_id', ForeignKey('questions.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id = mapped_column(ForeignKey("questions.id"))
    stdout: Mapped[str]
    time: Mapped[float]
    memory: Mapped[int]
    stderr: Mapped[str | None]
    token: Mapped[str]
    compile_output: Mapped[str | None]
    message: Mapped[str | None]
    status_id: Mapped[int]
    status_description: Mapped[str]
    created_at: Mapped[datetime]
    finished_at: Mapped[datetime]


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    tags: Mapped[list["Tag"]] = relationship(
        secondary=question_tag_association)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
