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


class HiddenSize(Base):
    __tablename__ = "hidden_sizes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    params_id = mapped_column(ForeignKey("parameters.id"))
    size: Mapped[int]


class Parameters(Base):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey("solutions.id"))
    solution: Mapped["Solution"] = relationship(
        back_populates="params", foreign_keys=[solution_id])
    type: Mapped[str]
    input_size: Mapped[int]
    output_size: Mapped[int]
    hidden_sizes: Mapped[list[HiddenSize]] = relationship()
    activation: Mapped[str]
    dropout: Mapped[float]
    batch_norm: Mapped[bool]


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id = mapped_column(ForeignKey("questions.id"))
    params: Mapped[Parameters] = relationship(back_populates="solution")
    content: Mapped[str]


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
