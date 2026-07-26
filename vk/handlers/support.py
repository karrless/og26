from email import message

from vkbottle.bot import Message, MessageEvent
from vkbottle.dispatch.rules.base import PeerRule, StateRule, StateGroupRule, FromPeerRule, CommandRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types import GroupEventType

from config import VK_MODERATOR_CHAT_PEER_ID
from core.content import texts
from core.content.keyboards import MENU_KEYBOARD, CANCEL_KEYS
from core.content.texts import CANCEL_BUTTON, MAIN_EXIT_WORDS
from core.db.models import Topic, User
from core.errors import CancelInputError
from core.keyboards import build_vk_keyboard
from core.services import SupportService
from vk.fsm import SupportStates, state_dispenser, wm
from vk.handlers import menu
from vk.middlewares.user import UserMiddleware
from vk.utils import ask_text

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False), StateGroupRule(state_group=SupportStates)]
bl.message_view.register_middleware(UserMiddleware)
bl.vbml_ignore_case = True

bl_support = BotLabeler()
bl_support.auto_rules=[PeerRule(from_chat=True), FromPeerRule(VK_MODERATOR_CHAT_PEER_ID)]
support_service = SupportService()

@bl.message()
async def in_support_mode(message: Message, user: User):
    if message.text.lower() in MAIN_EXIT_WORDS:
        return await menu.start_message(message, user)

async def get_own_question(message: Message, topic: Topic | None, user: User):
    # Спрашиваем вопрос
    await message.answer(texts.SUPPORT_ASK_QUESTION, keyboard=build_vk_keyboard([CANCEL_KEYS]))

    while True:
        question_message, _ = await wm.wait(bl.message_view, message)
        if question_message.text == CANCEL_BUTTON:
            raise CancelInputError()
        if question_message.text.strip() or question_message.attachments:
            break
        await message.answer(texts.SUPPORT_EMPTY_QUESTION)

    await support_service.create_ticket(
        user_id=user.id,
        topic_id=topic.id if topic else None,
        question_text=question_message.text or "[вложение]",
        source_peer_id=message.peer_id,
        conversation_message_id=question_message.conversation_message_id,
    )
    # Говорим, что вопрос приняли
    await message.answer(texts.SUPPORT_ENTERED)
    await message.answer(texts.SUPPORT_MODE)
    await state_dispenser.set(message.peer_id, SupportStates.IN_SUPPORT)
    return

@bl_support.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def on_ticket_button(event: MessageEvent):
    action = (event.payload or {}).get("action", "")
    if not action.startswith("ticket:"):
        return

    _, kind, ticket_id_raw = action.split(":")
    ticket_id = int(ticket_id_raw)

    if kind == "take":
        await support_service.take_ticket(ticket_id, moderator_vk_id=event.user_id)
    elif kind == "close":
        await _close_and_notify(ticket_id)


@bl_support.message( CommandRule(("закрыть", 1)))
async def close_by_command(message: Message, args):
    await _close_and_notify(int(args[0]))


async def _close_and_notify(ticket_id: int):
    ticket = await support_service.close_ticket(ticket_id)
    if ticket is None:
        return
    from vk.fsm import state_dispenser
    from core.db.repositories import UserRepository
    from core.db.engine import AsyncSessionFactory

    async with AsyncSessionFactory() as session:
        user = await UserRepository(session).get_by_id(ticket.user_id)
    if user and user.vk_id:
        await support_service.notify_user_closed(user.vk_id)
        await state_dispenser.delete(user.vk_id)