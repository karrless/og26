# core/keyboards/tg_adapter.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.content.keyboards import Button, MAX_ROWS_DEFAULT, MAX_BUTTONS_PER_ROW, ButtonColor
from core.content.texts import CANCEL_BUTTON

_COLOR_MAP = {
    ButtonColor.PRIMARY: 'primary',
    ButtonColor.SECONDARY: None,
    ButtonColor.POSITIVE: 'success',
    ButtonColor.NEGATIVE: 'danger',
    None: None
}

def build_tg_keyboard(rows: list[list[Button]], cancel: bool = False) -> ReplyKeyboardMarkup:
    if cancel:
        rows = [*rows, [Button(CANCEL_BUTTON, "cancel")]]

    if len(rows) > MAX_ROWS_DEFAULT:
        raise ValueError(f"Слишком много строк в клавиатуре: {len(rows)} > {MAX_ROWS_DEFAULT}")
    for row in rows:
        if len(row) > MAX_BUTTONS_PER_ROW:
            raise ValueError(f"Слишком много кнопок в строке: {len(row)} > {MAX_BUTTONS_PER_ROW}")

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn.text, style=_COLOR_MAP.get(btn.color)) for btn in row] for row in rows],
        resize_keyboard=True,
    )