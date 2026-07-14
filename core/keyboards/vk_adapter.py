from vkbottle import Keyboard, KeyboardButtonColor, Text

from core.content.keyboards import Button, ButtonColor, MAX_ROWS_DEFAULT, MAX_ROWS_INLINE, MAX_BUTTONS_PER_ROW
from core.content.texts import CANCEL_BUTTON

_COLOR_MAP = {
    ButtonColor.PRIMARY: KeyboardButtonColor.PRIMARY,
    ButtonColor.SECONDARY: KeyboardButtonColor.SECONDARY,
    ButtonColor.POSITIVE: KeyboardButtonColor.POSITIVE,
    ButtonColor.NEGATIVE: KeyboardButtonColor.NEGATIVE,
    None: None
}


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
            color = _COLOR_MAP.get(btn.color)
            kb.add(Text(btn.text, payload={"action": btn.action}), color=color)
        kb.row()
    return kb