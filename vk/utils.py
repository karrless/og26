from typing import Any, Optional

from vkbottle import Keyboard, KeyboardButtonColor
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.tools import WaiterMachine

from core.content.keyboards import Button
from core.content.texts import CANCEL_BUTTON
from core.keyboards import build_vk_keyboard
from core.pagination import Paginator, build_paginated_keyboard
from core.errors import CancelInputError


async def ask_text(bl: BotLabeler, wm: WaiterMachine, message: Message, validator, keyboard: Optional[Keyboard] = None) -> str:
    """Спрашивает текст и переспрашивает, пока validator не пройдёт."""
    while True:
        m, _ = await wm.wait(bl.message_view, message)
        if m.text.lower() == CANCEL_BUTTON.lower():
            raise CancelInputError()
        try:
            result = validator(m.text)
            return await result if hasattr(result, "__await__") else result
        except Exception as e:
            await message.answer(str(e), keyboard=keyboard)


async def ask_button(bl: BotLabeler, wm: WaiterMachine, message: Message, action_prefix: str) -> str:
    """Ждёт нажатие обычной кнопки с payload {"action": "<prefix>:<value>"}."""
    while True:
        m, _ = await wm.wait(bl.message_view, message)
        if m.text.lower() == CANCEL_BUTTON.lower():
            raise CancelInputError()
        payload = m.get_payload_json() or {}
        action = payload.get("action", "")
        if action.startswith(f"{action_prefix}:"):
            return action.split(":")[-1]
        # нажата кнопка с прошлого шага / случайный текст — просто игнор, ждём дальше


async def ask_paginated_choice(bl: BotLabeler,
                               wm: WaiterMachine,
                               message: Message,
                               text: str,
                               items: dict[str, str],
                               prefix: str,
                               columns: int = 1,
                               color: KeyboardButtonColor = KeyboardButtonColor.PRIMARY
                               ) -> Any | None:
    """

    :param wm: WaiterMachine
    :param bl: BotLabeler
    :param message: сообщение
    :param text: Текст отправляемого сообщения в пагинации
    :param items: Названия кнопок
    :param prefix: Префикс пагинации
    :param columns: Количество столбцов кнопок
    :param color: Цвет, который будет у кнопок
    :return:
    """
    entries = list(items.items())
    paginator = Paginator(entries, columns=columns)
    page_num = 1

    while True:
        page = paginator.get_page(page_num)
        rows = build_paginated_keyboard(page, lambda entry: Button(entry[1], f"{prefix}:pick:{entry[0]}", color), prefix=prefix, columns=columns)
        await message.answer(text, keyboard=build_vk_keyboard(rows, cancel=True))

        m, _ = await wm.wait(bl.message_view, message)
        payload = m.get_payload_json() or {}
        action = payload.get("action", "")

        if action == "cancel":
            raise CancelInputError()
        if action.startswith(f"{prefix}:pick:"):
            return action.split(":", 2)[2]
        if action.startswith(f"{prefix}:page:"):
            page_num = int(action.split(":")[-1])
            continue
