from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.content import texts
from core.content.keyboards import MENU_KEYBOARD
from core.content.texts import CANCEL_BUTTON
from core.keyboards import build_tg_keyboard
from core.keyboards.tg_adapter import build_tg_inline_keyboard
from tg.utils import reply

router = Router()

router.message.filter(F.chat.is_direct_messages == True)  # noqa: E712 — работаем только с DM канала


@router.message(CommandStart())
@router.message((F.text == CANCEL_BUTTON) | (F.text.lower() == "начать"))
async def start_message(message: Message, state: FSMContext):
    await state.clear()
    await reply(message, texts.MENU_TG, reply_markup=build_tg_inline_keyboard(MENU_KEYBOARD))