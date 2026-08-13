from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class RoomAssignment(Base):
    __tablename__ = "room_assignments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cipher: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    comfort: Mapped[str]
    room_number: Mapped[str]