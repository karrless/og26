from aiogram.types import Message, CallbackQuery


def _dm_topic_id(message: Message) -> int | None:
    return message.direct_messages_topic.topic_id if message.direct_messages_topic else None


async def reply(message: Message, text: str, **kwargs):
    """Универсальный ответ: работает и в обычной личке, и в Direct Messages канала."""
    return await message.answer(text, direct_messages_topic_id=_dm_topic_id(message), **kwargs)

async def edit(callback: CallbackQuery, text: str, **kwargs):
    """Правим то же самое сообщение (не нужен topic_id — редактируем уже существующее)."""
    return await callback.message.edit_text(text, **kwargs)


async def strip_keyboard(message: Message, message_id: int) -> None:
    """Убирает инлайн-клавиатуру у уже отправленного prompt-сообщения."""
    try:
        await message.bot.edit_message_reply_markup(
            chat_id=message.chat.id, message_id=message_id, reply_markup=None,
        )
    except Exception:
        pass