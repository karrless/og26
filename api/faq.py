from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.auth import require_auth
from core.db.engine import AsyncSessionFactory
from core.db.repositories import TopicRepository, SubtopicRepository, QuestionRepository

router = APIRouter(prefix="/faq", dependencies=[Depends(require_auth)])


class TopicIn(BaseModel):
    title: str


class SubtopicIn(BaseModel):
    title: str
    topic_id: int


class QuestionIn(BaseModel):
    answer: str
    subtopic_id: int
    attachment: str | None = None


# --- Topics ---
@router.get("/topics")
async def list_topics():
    async with AsyncSessionFactory() as session:
        return await TopicRepository(session).get_all_full()


@router.post("/topics")
async def create_topic(data: TopicIn):
    async with AsyncSessionFactory() as session:
        return await TopicRepository(session).create(title=data.title)


@router.put("/topics/{topic_id}")
async def update_topic(topic_id: int, data: TopicIn):
    async with AsyncSessionFactory() as session:
        repo = TopicRepository(session)
        topic = await repo.get_by_id(topic_id)
        if topic is None:
            raise HTTPException(404, "Тема не найдена")
        return await repo.update(topic, title=data.title)


@router.delete("/topics/{topic_id}")
async def delete_topic(topic_id: int):
    async with AsyncSessionFactory() as session:
        repo = TopicRepository(session)
        topic = await repo.get_by_id(topic_id)
        if topic is None:
            raise HTTPException(404, "Тема не найдена")
        await repo.delete(topic)
        return {"ok": True}


# --- Subtopics ---
@router.post("/subtopics")
async def create_subtopic(data: SubtopicIn):
    async with AsyncSessionFactory() as session:
        return await SubtopicRepository(session).create(title=data.title, topic_id=data.topic_id)


@router.put("/subtopics/{subtopic_id}")
async def update_subtopic(subtopic_id: int, data: SubtopicIn):
    async with AsyncSessionFactory() as session:
        repo = SubtopicRepository(session)
        subtopic = await repo.get_by_id(subtopic_id)
        if subtopic is None:
            raise HTTPException(404, "Подтема не найдена")
        return await repo.update(subtopic, title=data.title, topic_id=data.topic_id)


@router.delete("/subtopics/{subtopic_id}")
async def delete_subtopic(subtopic_id: int):
    async with AsyncSessionFactory() as session:
        repo = SubtopicRepository(session)
        subtopic = await repo.get_by_id(subtopic_id)
        if subtopic is None:
            raise HTTPException(404, "Подтема не найдена")
        await repo.delete(subtopic)
        return {"ok": True}


# --- Questions ---
@router.post("/questions")
async def create_question(data: QuestionIn):
    async with AsyncSessionFactory() as session:
        return await QuestionRepository(session).create(
            answer=data.answer, subtopic_id=data.subtopic_id, attachment=data.attachment,
        )


@router.put("/questions/{question_id}")
async def update_question(question_id: int, data: QuestionIn):
    async with AsyncSessionFactory() as session:
        repo = QuestionRepository(session)
        question = await repo.get_by_id(question_id)
        if question is None:
            raise HTTPException(404, "Вопрос не найден")
        return await repo.update(question, answer=data.answer, subtopic_id=data.subtopic_id, attachment=data.attachment)


@router.delete("/questions/{question_id}")
async def delete_question(question_id: int):
    async with AsyncSessionFactory() as session:
        repo = QuestionRepository(session)
        question = await repo.get_by_id(question_id)
        if question is None:
            raise HTTPException(404, "Вопрос не найден")
        await repo.delete(question)
        return {"ok": True}