from core.db.engine import AsyncSessionFactory
from core.db.models import User, RoomAssignment
from core.db.repositories import RoomAssignmentRepository, UserRepository


class RoommateAlreadySetError(Exception):
    pass


class RoommateCipherNotFoundError(Exception):
    pass


class RoommateService:
    def __init__(self, session_factory=AsyncSessionFactory):
        self.session_factory = session_factory

    async def assign_cipher(self, user_id: int, cipher: int) -> tuple[User, list[User], RoomAssignment]:
        async with self.session_factory() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_id(user_id)

            if user.cipher is not None:
                raise RoommateAlreadySetError()

            room_repo = RoomAssignmentRepository(session)
            room = await room_repo.get_by_cipher(cipher)
            if room is None:
                raise RoommateCipherNotFoundError()

            if await user_repo.get_by_cipher(cipher) is not None:
                raise RoommateAlreadySetError()

            user = await user_repo.update(user, cipher=cipher)

            roommate_ciphers = [
                c for c in await room_repo.get_ciphers_in_room(room.comfort, room.room_number)
                if c != cipher
            ]
            roommates = await user_repo.get_by_ciphers(roommate_ciphers)

        return user, roommates, room

    async def get_roommates(self, user: User) -> tuple[list[User], RoomAssignment | None]:
        if user.cipher is None:
            return [], None
        async with self.session_factory() as session:
            room_repo = RoomAssignmentRepository(session)
            room = await room_repo.get_by_cipher(user.cipher)
            if room is None:
                return [], None
            ciphers = [
                c for c in await room_repo.get_ciphers_in_room(room.comfort, room.room_number)
                if c != user.cipher
            ]
            roommates = await UserRepository(session).get_by_ciphers(ciphers)
        return roommates, room