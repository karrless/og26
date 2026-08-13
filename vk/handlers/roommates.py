from loguru import logger
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule
from vkbottle.framework.labeler import BotLabeler
import asyncio

from core.content import texts, CANCEL_KEYS
from core.content.texts import ROOMMATES_BUTTON
from core.db.models import User
from core.errors import CancelInputError, FormValidationError
from core.keyboards import build_vk_keyboard
from core.services import RoommateService, SheetsService
from core.services.room_service import RoommateAlreadySetError, RoommateCipherNotFoundError
from vk.fsm import wm
from vk.handlers import menu
from vk.middlewares.user import UserMiddleware
from vk.utils import ask_text

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserMiddleware)

roommate_service = RoommateService()
sheets_service = SheetsService()


def _mention(user: User) -> str:
    name = f"{user.name or ''} {user.surname or ''}".strip() or "Профиль"
    return f"[id{user.vk_id}|{name}]"


def _validate_cipher(t: str) -> int:
    t = t.strip()
    if not t.isdigit():
        raise FormValidationError(texts.ROOMMATES_CIPHER_INVALID)
    return int(t)


async def _notify_roommate(message: Message, roommate: User, new_user: User) -> None:
    if not roommate.vk_id:
        return
    try:
        await message.ctx_api.messages.send(
            peer_id=roommate.vk_id,
            message=texts.ROOMMATES_NEW_NEIGHBOR.format(mention=_mention(new_user)),
            random_id=__import__("random").randint(1, 2 ** 31 - 1),
        )
    except Exception as ex:
        logger.error(ex)


@bl.message(text=ROOMMATES_BUTTON.lower())
async def roommates(message: Message, user: User):
    try:
        if user.cipher is None:
            await message.answer(texts.ROOMMATES_ASK_CIPHER, keyboard=build_vk_keyboard([CANCEL_KEYS]))
            cipher = await ask_text(bl, wm, message, _validate_cipher, CANCEL_KEYS)

            try:
                user, existing_roommates, room = await roommate_service.assign_cipher(user.id, cipher)
            except RoommateCipherNotFoundError:
                return await message.answer(texts.ROOMMATES_CIPHER_NOT_FOUND)
            except RoommateAlreadySetError:
                return await message.answer(texts.ROOMMATES_CIPHER_TAKEN)

            # проверка анкеты в гугл-таблице уходит фоном, не блокирует остальной флоу
            _run_in_background(_check_form_and_notify(message, cipher, message.peer_id))

            for roommate in existing_roommates:
                await _notify_roommate(message, roommate, user)

            text = texts.ROOMMATES_YOUR_ROOM.format(comfort=room.comfort, room_number=room.room_number)
            if existing_roommates:
                links = "\n".join(_mention(r) for r in existing_roommates)
                text += f"\n\n{texts.ROOMMATES_LIST_HEADER}\n{links}"
            else:
                text += f"\n\n{texts.ROOMMATES_NONE_YET}"
            await message.answer(text)
            return

        roommates_list, room = await roommate_service.get_roommates(user)
        if room is None:
            return await message.answer(texts.ROOMMATES_NONE_YET)

        await message.answer(texts.ROOMMATES_YOUR_ROOM.format(comfort=room.comfort, room_number=room.room_number))

        if not roommates_list:
            return await message.answer(texts.ROOMMATES_NONE_YET)

        links = "\n".join(_mention(r) for r in roommates_list)
        await message.answer(f"{texts.ROOMMATES_LIST_HEADER}\n{links}")

    except CancelInputError:
        pass
    finally:
        await menu.start_message(message, user)


_background_tasks: set[asyncio.Task] = set()

async def _check_form_and_notify(message: Message, cipher: int, peer_id: int) -> None:
    try:
        in_form = await sheets_service.find_cipher(str(cipher))
        if not in_form:
            await message.ctx_api.messages.send(
                peer_id=peer_id,
                message=texts.ROOMMATES_FILL_FORM_REMINDER,
                random_id=__import__("random").randint(1, 2 ** 31 - 1),
            )
    except Exception as ex:
        logger.error(ex)


def _run_in_background(coro) -> None:
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
