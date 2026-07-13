from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.content.keyboards import Button


def build_tg_keyboard(rows: list[list[Button]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=b.text, callback_data=b.action) for b in row]
        for row in rows
    ])
