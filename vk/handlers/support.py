from email import message

from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule, StateRule, StateGroupRule
from vkbottle.framework.labeler import BotLabeler

from core.content import texts
from core.content.keyboards import MENU_KEYBOARD, CANCEL_KEYS
from core.content.texts import CANCEL_BUTTON
from core.db.models import Topic, User
from core.errors import CancelInputError
from core.keyboards import build_vk_keyboard
from vk.fsm import SupportStates, state_dispenser, wm
from vk.handlers import menu
from vk.utils import ask_text

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False), StateGroupRule(state_group=SupportStates)]
bl.vbml_ignore_case = True


@bl.message()
async def in_support_mode(message: Message):
    return


async def get_own_question(message: Message, topic: Topic | None, user: User):
    # Спрашиваем вопрос
    await message.answer(texts.SUPPORT_ASK_QUESTION, keyboard=build_vk_keyboard([CANCEL_KEYS]))
    question_text = await ask_text(bl, wm, message, lambda t: t.strip(), CANCEL_KEYS)

    # TODO: Оповещение + БД

    # Говорим, что вопрос приняли
    await message.answer(texts.SUPPORT_ENTERED)
    await message.answer(texts.SUPPORT_MODE)
    await state_dispenser.set(message.peer_id, SupportStates.IN_SUPPORT)
    return

