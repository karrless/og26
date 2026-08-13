from sqlalchemy import select, delete

from core.db.models import RoomAssignment
from core.db.repositories.base import BaseRepository


class RoomAssignmentRepository(BaseRepository[RoomAssignment]):
    model = RoomAssignment

    async def get_by_cipher(self, cipher: int) -> RoomAssignment | None:
        result = await self.session.execute(
            select(RoomAssignment).where(RoomAssignment.cipher == cipher)
        )
        return result.scalar_one_or_none()

    async def get_ciphers_in_room(self, comfort: str, room_number: str) -> list[int]:
        result = await self.session.execute(
            select(RoomAssignment.cipher).where(
                RoomAssignment.comfort == comfort,
                RoomAssignment.room_number == room_number,
                )
        )
        return list(result.scalars().all())

    async def clear_all(self) -> None:
        await self.session.execute(delete(RoomAssignment))