from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule, CommandRule
from vkbottle.framework.labeler import BotLabeler

from core.content import CANCEL_BUTTON, texts
from core.content.keyboards import MENU_KEYBOARD
from core.content.texts import MAIN_EXIT_WORDS
from core.db.models import User
from core.keyboards import build_vk_keyboard
from core.services import SupportService
from vk.fsm import state_dispenser, SupportStates
from vk.middlewares.user import UserMiddleware



bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserMiddleware)
support_service = SupportService()

default_bl = BotLabeler()
default_bl.auto_rules = [PeerRule(from_chat=False)]

@bl.message(text=MAIN_EXIT_WORDS)
@default_bl.message()
async def start_message(message: Message,
                        user: User):
    state = await state_dispenser.get(message.peer_id)
    if state:
        match state.state:
            case SupportStates.IN_SUPPORT:
                await support_service.close_open_ticket_by_user(user.id)
    await state_dispenser.delete(message.peer_id)
    return await message.answer(texts.MENU_VK, keyboard=build_vk_keyboard(MENU_KEYBOARD))

debug_bl = BotLabeler()
debug_bl.auto_rules = [PeerRule(from_chat=True)]

@debug_bl.message(CommandRule("og_debug"))
async def debug_message(message: Message):
    await message.answer(message)
