from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vk_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    vk_screen_name: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    tg_id: Mapped[Optional[int]] = mapped_column(unique=True, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    surname: Mapped[Optional[str]] = mapped_column(nullable=True)
    cipher: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)
