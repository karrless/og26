from vkbottle import Keyboard, Text

from core.content.keyboards import Button, MAX_ROWS_DEFAULT, MAX_ROWS_INLINE, MAX_BUTTONS_PER_ROW
from core.content.texts import CANCEL_BUTTON


def build_vk_keyboard(rows: list[list[Button]], inline: bool = False, cancel: bool = False) -> Keyboard:
    if cancel:
        rows = [*rows, [Button(CANCEL_BUTTON, "cancel")]]

    max_rows = MAX_ROWS_INLINE if inline else MAX_ROWS_DEFAULT
    if len(rows) > max_rows:
        raise ValueError(f"Слишком много строк в клавиатуре: {len(rows)} > {max_rows}")
    for row in rows:
        if len(row) > MAX_BUTTONS_PER_ROW:
            raise ValueError(f"Слишком много кнопок в строке: {len(row)} > {MAX_BUTTONS_PER_ROW}")

    kb = Keyboard(inline=inline)
    for row in rows:
        for btn in row:
            kb.add(Text(btn.text, payload={"action": btn.action}), color=btn.color)
        kb.row()
    return kb