# core/keyboards/tg_adapter.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from core.content.keyboards import Button, MAX_ROWS_DEFAULT, MAX_BUTTONS_PER_ROW, ButtonColor, BACK_KEYS, CANCEL_KEYS
from core.content.texts import CANCEL_BUTTON, BACK_BUTTON

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

def build_tg_inline_keyboard(
        rows: list[list[Button]], cancel: bool = False, back: bool = False
) -> InlineKeyboardMarkup:
    extra_keys = []
    if back:
        extra_keys = BACK_KEYS
    if cancel:
        extra_keys = [*extra_keys, *CANCEL_KEYS]

    if len(extra_keys):
        rows = [*rows, extra_keys]
    if len(rows) > MAX_ROWS_DEFAULT:
        raise ValueError(f"Слишком много строк: {len(rows)} > {MAX_ROWS_DEFAULT}")
    for row in rows:
        if len(row) > MAX_BUTTONS_PER_ROW:
            raise ValueError(f"Слишком много кнопок в строке: {len(row)} > {MAX_BUTTONS_PER_ROW}")

    def _to_tg_button(btn: Button) -> InlineKeyboardButton:
        if btn.url:
            return InlineKeyboardButton(text=btn.text, url=btn.url)
        return InlineKeyboardButton(text=btn.text, callback_data=btn.action)

    return InlineKeyboardMarkup(inline_keyboard=[
        [_to_tg_button(btn) for btn in row]
        for row in rows
    ])