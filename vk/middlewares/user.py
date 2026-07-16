from vkbottle.dispatch.middlewares import BaseMiddleware

from core.db import AsyncSessionFactory
from core.db.repositories import UserRepository
from core.services.user_service import UserService
from core.services.vk_resolver import get_vk_user

class UserMiddleware(BaseMiddleware):

    async def pre(self):
        message = self.event

        # сообщения от групп
        if message.from_id <= 0:
            return

        vk_user = await get_vk_user(
            message.from_id
        )

        user = await UserService().get_or_create_by_vk_id(
            vk_id=message.from_id,
            vk_screen_name=vk_user.domain if vk_user else None,
            name=vk_user.first_name if vk_user else None,
            surname=vk_user.last_name if vk_user else None,
        )

        self.send({
            "user": user,
        })