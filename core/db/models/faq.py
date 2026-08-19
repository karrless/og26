from typing import Optional

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]

    subtopics: Mapped[list["Subtopic"]] = relationship(back_populates="topic", cascade="all, delete-orphan", passive_deletes=True)


class Subtopic(Base):
    __tablename__ = "subtopics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))

    topic: Mapped["Topic"] = relationship(back_populates="subtopics")
    questions: Mapped[list["Question"]] = relationship(back_populates="subtopic", cascade="all, delete-orphan", passive_deletes=True)


class Question(Base):
    __tablename__ = "questions"

    __table_args__ = (
        CheckConstraint(
            "(topic_id IS NOT NULL) <> (subtopic_id IS NOT NULL)",
            name="ck_question_parent",
        ),
        Index("uq_question_subtopic", "subtopic_id", unique=True, postgresql_where=text("subtopic_id IS NOT NULL")),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    answer: Mapped[str]
    attachment: Mapped[Optional[str]] = mapped_column(nullable=True)

    subtopic_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=True,
    )
    subtopic: Mapped[Optional["Subtopic"]] = relationship(back_populates="questions")