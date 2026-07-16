from core.db import AsyncSessionFactory
from core.db.models import Topic, Subtopic
from core.db.repositories import TopicRepository, SubtopicRepository


class FaqService:
    def __init__(self, session_factory=AsyncSessionFactory):
        self.session_factory = session_factory

    async def get_topics(self) -> list[Topic]:
        async with self.session_factory() as session:
            return await TopicRepository(session).get_all()

    async def get_topic_full(self, topic_id: int) -> Topic | None:
        async with self.session_factory() as session:
            return await TopicRepository(session).get_full(topic_id)

    async def get_subtopic_full(self, subtopic_id: int) -> Subtopic | None:
        async with self.session_factory() as session:
            return await SubtopicRepository(session).get_full(subtopic_id)