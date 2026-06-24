from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vk_id: Mapped[int] = mapped_column(unique=True)
    tg_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    # room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), nullable=True)
    # comfort_name: Mapped[str] = mapped_column(ForeignKey('comforts.name'), nullable=True)
