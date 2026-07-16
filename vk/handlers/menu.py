from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule
from vkbottle.framework.labeler import BotLabeler

from core.content import CANCEL_BUTTON, texts
from core.content.keyboards import MENU_KEYBOARD
from core.db.models import User
from core.keyboards import build_vk_keyboard
from vk.fsm import state_dispenser, SupportStates
from vk.middlewares.user import UserMiddleware

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserMiddleware)

default_bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]

@bl.message(text=(CANCEL_BUTTON, 'Начать', 'Start'))
@default_bl.message()
async def start_message(message: Message,
                        user: User):
    state = await state_dispenser.get(message.peer_id)
    match state:
        case SupportStates.IN_SUPPORT:
            # TODO: Закрыть вопрос
            pass
    await state_dispenser.delete(message.peer_id)
    await message.answer(f"Ты {user.vk_id} {user.vk_screen_name} {user.name} {user.surname}")
    return await message.answer(texts.MENU_VK, keyboard=build_vk_keyboard(MENU_KEYBOARD))