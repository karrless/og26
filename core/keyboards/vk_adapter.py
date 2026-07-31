from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback, OpenLink

from core.content import CANCEL_KEYS
from core.content.keyboards import Button, ButtonColor, MAX_ROWS_DEFAULT, MAX_ROWS_INLINE, MAX_BUTTONS_PER_ROW, \
    BACK_KEYS
from core.content.texts import CANCEL_BUTTON, BACK_BUTTON

_COLOR_MAP = {
    ButtonColor.PRIMARY: KeyboardButtonColor.PRIMARY,
    ButtonColor.SECONDARY: KeyboardButtonColor.SECONDARY,
    ButtonColor.POSITIVE: KeyboardButtonColor.POSITIVE,
    ButtonColor.NEGATIVE: KeyboardButtonColor.NEGATIVE,
    None: None
}


def build_vk_keyboard(
        rows: list[list[Button]],
        inline: bool = False,
        cancel: bool = False,
        back: bool = False
) -> Keyboard:
    extra_keys = []
    if back:
        extra_keys = BACK_KEYS
    if cancel:
        extra_keys = [*extra_keys, *CANCEL_KEYS]

    if len(extra_keys):
        rows = [*rows, extra_keys]

    max_rows = MAX_ROWS_INLINE if inline else MAX_ROWS_DEFAULT
    if len(rows) > max_rows:
        raise ValueError(f"Слишком много строк в клавиатуре: {len(rows)} > {max_rows}")
    for row in rows:
        if len(row) > MAX_BUTTONS_PER_ROW:
            raise ValueError(f"Слишком много кнопок в строке: {len(row)} > {MAX_BUTTONS_PER_ROW}")

    kb = Keyboard(inline=inline)
    button_cls = Callback if inline else Text

    for row in rows:
        for btn in row:
            if btn.url:
                kb.add(OpenLink(btn.url, btn.text))
            else:
                color = _COLOR_MAP.get(btn.color)
                kb.add(button_cls(btn.text, payload={"action": btn.action}), color=color)
        kb.row()
    return kb