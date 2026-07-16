from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.db.models import Question, Subtopic, Topic
from core.db.repositories import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    model = Question

    async def get_by_subtopic(self, subtopic_id: int) -> list[Question]:
        """Получить все вопросы, принадлежащие указанной подтеме"""
        result = await self.session.execute(
            select(Question).where(Question.subtopic_id == subtopic_id)
        )
        return list(result.scalars().all())

class SubtopicRepository(BaseRepository[Subtopic]):
    model = Subtopic

    async def get_full(self, subtopic_id: int) -> Subtopic | None:
        """Получить подтему вместе со всеми ее вопросами"""
        result = await self.session.execute(
            select(Subtopic)
            .options(selectinload(Subtopic.questions))
            .where(Subtopic.id == subtopic_id)
        )
        return result.scalar_one_or_none()

    async def get_by_topic(self, topic_id: int) -> list[Subtopic]:
        """Получить все подтемы указанной темы"""
        result = await self.session.execute(
            select(Subtopic).where(Subtopic.topic_id == topic_id)
        )
        return list(result.scalars().all())


class TopicRepository(BaseRepository[Topic]):
    model = Topic

    async def get_full(self, topic_id: int) -> Topic | None:
        """Получить тему вместе с ее вопросами, подтемами и вопросами этих подтем"""
        result = await self.session.execute(
            select(Topic)
            .options(
                selectinload(Topic.subtopics).selectinload(Subtopic.questions),
            )
            .where(Topic.id == topic_id)
        )
        return result.scalar_one_or_none()

    async def get_all_full(self) -> list[Topic]:
        """Получить полное дерево FAQ:
            все темы, их вопросы, подтемы и вопросы подтем"""
        result = await self.session.execute(
            select(Topic).options(
                selectinload(Topic.subtopics).selectinload(Subtopic.questions),
            )
        )
        return list(result.scalars().unique().all())