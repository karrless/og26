from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base

Model = TypeVar("Model", bound=Base)

class BaseRepository(Generic[Model]):
    model: Type[Model]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Model | None:
        """Получить объект по его первичному ключу"""
        return await self.session.get(self.model, id)

    async def get_all(self) -> list[Model]:
        """Получить все объекты данной модели"""
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Model:
        """Создать новый объект и сохранить его в базе"""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: Model) -> None:
        """Удалить объект из базы"""
        await self.session.delete(obj)
        await self.session.commit()

    async def update(self, obj: Model, **kwargs) -> Model:
        """Обновить указанные поля объекта и сохранить изменения"""
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

