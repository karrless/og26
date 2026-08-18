from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle.tools import WaiterMachine

from core.content import texts, CANCEL_KEYS
from core.content.keyboards import DIRECTIONS, YES_NO_KEYBOARD
from core.content.texts import FORM_BUTTON
from core.db.models import User
from core.keyboards import build_vk_keyboard
from core.services.form_service import FormService, FormData
from core.services import SheetsService
from core.errors import CancelInputError
from vk.fsm import wm
from vk.handlers import menu
from vk.middlewares.user import UserMiddleware
from vk.utils import ask_text, ask_button, ask_paginated_choice

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserMiddleware)

form_service = FormService(SheetsService())  # создаётся один раз


@bl.message(command="form")
@bl.message(text=FORM_BUTTON.lower())
async def form(message: Message, user: User):
    cancel_keys = build_vk_keyboard([CANCEL_KEYS])
    await message.answer(texts.FORM_ASK_FIO, keyboard=cancel_keys)
    fio = await ask_text(bl, wm, message, form_service.validate_fio, cancel_keys)

    vk_id = await form_service.resolve_own_vk_id(message.peer_id)

    await message.answer(texts.FORM_ASK_NUMBER, keyboard=cancel_keys)
    number = await ask_text(bl, wm, message, form_service.validate_unique_number, cancel_keys)

    yes_no_keyboard = build_vk_keyboard(YES_NO_KEYBOARD)
    await message.answer(texts.FORM_ASK_YES_NO, keyboard=yes_no_keyboard)
    yes_no = await ask_text(bl, wm, message, form_service.validate_yes_no, yes_no_keyboard)

    direction = await ask_paginated_choice(bl, wm, message, texts.FORM_ASK_DIRECTION, DIRECTIONS,
                                           prefix="direction")
    data = FormData(fio=fio, vk_id=vk_id, number=number, yes_no=yes_no, direction=str(direction))

    progress_message = await message.answer(texts.FORM_SUBMITTING)

    ok = await form_service.submit(data)

    await message.ctx_api.messages.edit(
        peer_id=progress_message.peer_id,
        cmid=progress_message.conversation_message_id,
        message=texts.FORM_DONE if ok else texts.FORM_NOT_FOUND,
    )
    await menu.start_message(message, user)
