from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.content import texts
from core.content.keyboards import MENU_KEYBOARD
from core.content.texts import CANCEL_BUTTON
from core.keyboards import build_tg_keyboard

router = Router()


@router.message(CommandStart())
@router.message(F.text == CANCEL_BUTTON)
async def start_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.MENU_TG, reply_markup=build_tg_keyboard(MENU_KEYBOARD))