from typing import Optional

from core.db import AsyncSessionFactory
from core.db.models import User
from core.db.repositories import UserRepository


class UserService:
    def __init__(self, session_factory=AsyncSessionFactory):
        self.session_factory = session_factory

    async def get_or_create_by_vk_id(
            self,
            vk_id: int,
            vk_screen_name: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
    ) -> User:
        async with self.session_factory() as session:
            return await UserRepository(session).get_or_create_by_vk_id(vk_id, vk_screen_name, name, surname)
