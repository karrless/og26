from typing import Optional

from sqlalchemy import select, update

from core.db import Base
from core.db.models.user import User
from core.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_or_create_by_vk_id(
            self,
            vk_id: int,
            vk_screen_name: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
    ) -> User:
        """Найти пользователя по VK ID.

     Если пользователь отсутствует — создать нового.

     Если существует — обновить информацию о нем"""
        result = await self.session.execute(select(User).where(User.vk_id == vk_id))
        user = result.scalar_one_or_none()

        if user is None:
            user = User(vk_id=vk_id, vk_screen_name=vk_screen_name, name=name, surname=surname)
            self.session.add(user)
        else:
            user.vk_screen_name = vk_screen_name
            user.name = name
            user.surname = surname

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_or_create_by_tg_id(
            self,
            tg_id: int,
            name: Optional[str] = None,
            surname: Optional[str] = None,
    ) -> User:
        """Найти пользователя по Telegram ID.

    Если пользователь отсутствует — создать нового.

    Если существует — обновить информацию о нем"""
        result = await self.session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user is None:
            user = User(tg_id=tg_id, name=name, surname=surname)
            self.session.add(user)
        else:
            user.name = name
            user.surname = surname

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def merge_users(self, vk_user: User, tg_user: User) -> User:
        """Объединяет vk_user и tg_user: приоритет данных у vk_user,
        tg_user удаляется, его tg_id переносится на vk_user,
        все FK-связи на tg_user.id перепривязываются на vk_user.id."""
        if vk_user.id == tg_user.id:
            return vk_user

        vk_user.tg_id = tg_user.tg_id

        for mapper in Base.registry.mappers:
            related_model = mapper.class_
            if related_model is User:
                continue
            for column in mapper.columns:
                for fk in column.foreign_keys:
                    if fk.column.table is User.__table__:
                        await self.session.execute(
                            update(related_model)
                            .where(column == tg_user.id)
                            .values({column.name: vk_user.id})
                        )

        await self.session.delete(tg_user)
        await self.session.commit()
        await self.session.refresh(vk_user)
        return vk_user
