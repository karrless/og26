from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule
from vkbottle.framework.labeler import BotLabeler

from core.content import CANCEL_BUTTON, texts
from core.content.keyboards import MENU_KEYBOARD
from core.keyboards import build_vk_keyboard

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True

default_bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]

@bl.message(text=(CANCEL_BUTTON, 'Начать', 'Start'))
@default_bl.message()
async def start_message(message: Message):
    return await message.answer(texts.MENU_VK, keyboard=build_vk_keyboard(MENU_KEYBOARD))