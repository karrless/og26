from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db import Base

from .user import User

from .faq import Topic


class TicketStatus(PyEnum):
    OPEN = "open"
    TAKEN = "taken"
    CLOSED = "closed"


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[Optional[int]] = mapped_column(ForeignKey("topics.id"), nullable=True)

    question: Mapped[str]
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN)

    source_peer_id: Mapped[int] = mapped_column(BigInteger)  # <-- новое
    source_conversation_message_id: Mapped[int] = mapped_column(BigInteger)  # <-- новое

    moderator_vk_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    moderator_message_id: Mapped[Optional[int]] = mapped_column(nullable=True)  # для messages.edit

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    closed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
    topic: Mapped[Optional["Topic"]] = relationship()