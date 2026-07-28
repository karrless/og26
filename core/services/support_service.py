import json
import random
from datetime import datetime, timezone, time
from zoneinfo import ZoneInfo

import config
from config import MODER_LIMIT
from core.content import texts
from core.content.keyboards import Button, MENU_KEYBOARD
from core.content.texts import TICKET_CLOSE_BUTTON, TICKET_TAKE_BUTTON
from core.db.engine import AsyncSessionFactory
from core.db.models import SupportTicket, TicketStatus
from core.db.repositories import SupportTicketRepository, TopicRepository, UserRepository
from core.keyboards import build_vk_keyboard
from vk.api import api


class SupportService:
    def __init__(self, session_factory=AsyncSessionFactory):
        self.api = api
        self.session_factory = session_factory

    def _ticket_keyboard(self, ticket_id: int, taken: bool = False):
        buttons = [Button(TICKET_CLOSE_BUTTON, f"ticket:close:{ticket_id}")]
        if not taken:
            buttons.insert(0, Button(TICKET_TAKE_BUTTON, f"ticket:take:{ticket_id}"))
        return build_vk_keyboard([buttons], inline=True)

    async def create_ticket(
            self,
            user_id: int,
            topic_id: int | None,
            question_text: str,
            source_peer_id: int,
            conversation_message_id: int,
    ) -> SupportTicket:
        async with self.session_factory() as session:
            ticket = await SupportTicketRepository(session).create(
                user_id=user_id,
                topic_id=topic_id,
                question=question_text,
                status=TicketStatus.OPEN,
                source_peer_id=source_peer_id,
                source_conversation_message_id=conversation_message_id,
            )
            topic = await TopicRepository(session).get_by_id(topic_id) if topic_id else None
            ticket_id = ticket.id

        header = texts.TICKET_OPEN_TEXT.format(id=ticket_id, topic=topic.title if topic else "—")

        send_result = await self.api.messages.send(
            peer_ids=[config.VK_MODERATOR_CHAT_PEER_ID],
            message=header,
            keyboard=self._ticket_keyboard(ticket_id),
            forward=self._forward_json(ticket),
            random_id=random.randint(1, 2 ** 31 - 1),
        )
        moderator_cmid = send_result[0].conversation_message_id

        async with self.session_factory() as session:
            repo = SupportTicketRepository(session)
            ticket = await repo.get_by_id(ticket_id)
            ticket = await repo.update(ticket, moderator_message_id=moderator_cmid)
        return ticket

    async def take_ticket(self, ticket_id: int, moderator_vk_id: int) -> SupportTicket | None:
        async with self.session_factory() as session:
            repo = SupportTicketRepository(session)
            ticket = await repo.get_by_id(ticket_id)
            if ticket is None or ticket.status != TicketStatus.OPEN:
                return None
            ticket = await repo.update(ticket, status=TicketStatus.TAKEN, moderator_vk_id=moderator_vk_id)
            topic = await TopicRepository(session).get_by_id(ticket.topic_id) if ticket.topic_id else None

        text = texts.TICKET_TAKEN_NOTICE.format(
            id=ticket.id, topic=topic.title if topic else "—", question=ticket.question, vk_id=moderator_vk_id
        )
        await self.api.messages.edit(
            peer_id=config.VK_MODERATOR_CHAT_PEER_ID,
            conversation_message_id=ticket.moderator_message_id,
            message=text,
            keyboard=self._ticket_keyboard(ticket.id, taken=True),
            keep_forward_messages=1,
        )
        return ticket

    async def close_ticket(self, ticket_id: int) -> SupportTicket | None:
        async with self.session_factory() as session:
            repo = SupportTicketRepository(session)
            ticket = await repo.get_by_id(ticket_id)
            if ticket is None or ticket.status == TicketStatus.CLOSED:
                return None
            ticket = await repo.update(ticket, status=TicketStatus.CLOSED, closed_at=datetime.utcnow())

        await self.api.messages.edit(
            peer_id=config.VK_MODERATOR_CHAT_PEER_ID,
            conversation_message_id=ticket.moderator_message_id,
            message=texts.TICKET_CLOSED_TEXT.format(id=ticket.id, vk_id=ticket.moderator_vk_id),
            keyboard=build_vk_keyboard([], inline=True),
            keep_forward_messages=1,
        )
        return ticket

    async def close_open_ticket_by_user(self, user_id: int) -> SupportTicket | None:
        async with self.session_factory() as session:
            ticket = await SupportTicketRepository(session).get_open_by_user(user_id)
        if ticket is None:
            return None
        return await self.close_ticket(ticket.id)

    async def notify_user_closed(self, user_vk_peer_id: int) -> None:
        await self.api.messages.send(
            peer_id=user_vk_peer_id, message=texts.TICKET_CLOSED_FOR_USER, random_id=random.randint(0, user_vk_peer_id),
        )
        await self.api.messages.send(peer_id=user_vk_peer_id, message=texts.MENU_VK,
                                     keyboard=build_vk_keyboard(MENU_KEYBOARD),
                                     random_id=random.randint(0, user_vk_peer_id))

    async def has_reached_daily_limit(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            count = await SupportTicketRepository(session).count_today_by_user(user_id)
        return count >= MODER_LIMIT

    @staticmethod
    def _forward_json(ticket: SupportTicket) -> str:
        return json.dumps({
            "peer_id": ticket.source_peer_id,
            "conversation_message_ids": [ticket.source_conversation_message_id],
            "is_reply": False,
        })

    @staticmethod
    def is_within_working_hours() -> bool:

        MSK = ZoneInfo("Europe/Moscow")
        SUPPORT_HOURS_START = time(10, 0)
        SUPPORT_HOURS_END = time(22, 0)

        now = datetime.now(MSK).time()
        return SUPPORT_HOURS_START <= now < SUPPORT_HOURS_END