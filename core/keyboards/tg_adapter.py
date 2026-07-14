from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.content.keyboards import Button
from core.content.texts import CANCEL_BUTTON


def build_tg_keyboard(rows: list[list[Button]], cancel: bool = False) -> InlineKeyboardMarkup:
    if cancel:
        rows = [*rows, [Button(CANCEL_BUTTON, "cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=b.text, callback_data=b.action) for b in row]
        for row in rows
    ])
