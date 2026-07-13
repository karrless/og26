from vkbottle import Keyboard, Text

from core.content.keyboards import Button


def build_vk_keyboard(rows: list[list[Button]]) -> Keyboard:
    kb = Keyboard(inline=True)
    for row in rows:
        for btn in row:
            kb.add(Text(btn.text, payload={"action": btn.action}))
        kb.row()
    return kb