from loguru import logger
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import PeerRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle.tools import WaiterMachine

from core.content import texts, CANCEL_KEYS
from core.content.keyboards import OWN_QUESTION_KEYS
from core.content.texts import FAQ_BUTTON
from core.db.models import Topic, User
from core.errors import CancelInputError, GoBackError, ExtraActionSelected
from core.keyboards import build_vk_keyboard
from core.services import FaqService, SupportService
from vk.fsm import SupportStates, state_dispenser, wm
from vk.handlers import menu
from vk.handlers.support import get_own_question
from vk.middlewares.user import UserMiddleware
from vk.utils import ask_paginated_choice, ask_text

bl = BotLabeler()
bl.auto_rules = [PeerRule(from_chat=False)]
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserMiddleware)
faq_service = FaqService()
support_service = SupportService()

def _as_button_map(items, id_attr="id", title_attr="title") -> dict[str, str]:
    """dict {id_как_строка: алиас_для_кнопки (обрезан до 40 символов)}"""
    return {
        str(getattr(item, id_attr)): getattr(item, title_attr)[:40]
        for item in items
    }

@bl.message(text=FAQ_BUTTON.lower())
async def faq(message: Message, user: User):
    try:
        while True:
            # получаем и отправляем топики
            topics = await faq_service.get_topics()
            if not topics:
                await message.answer(texts.FAQ_EMPTY)
                break

            topic_id = await ask_paginated_choice(
                bl, wm, message, texts.FAQ_ASK_TOPIC, _as_button_map(topics), prefix="topic", columns=2,
            )

            # получаем и отправляем субтопики
            topic = await faq_service.get_topic_full(int(str(topic_id)))
            if topic is None or not topic.subtopics:
                continue
            try:
                while True:
                    subtopic_id = await ask_paginated_choice(
                        bl, wm, message, texts.FAQ_ASK_SUBTOPIC(topic.title), _as_button_map(topic.subtopics),
                        columns=2,
                        prefix="subtopic", back=True,
                        extra_buttons=OWN_QUESTION_KEYS,
                        extra_context={"topic": topic},
                    )
                    subtopic = await faq_service.get_subtopic_full(int(str(subtopic_id)))
                    if subtopic and subtopic.questions:
                        await message.answer(subtopic.questions[0].answer)
                    # после ответа — снова наверх внутреннего цикла: ждём следующую подтему/back/cancel
            except GoBackError:
                # обратно к списку тем (внешний while)
                continue
    # задать свой вопрос
    except ExtraActionSelected as ex:
        if not support_service.is_within_working_hours():
            await message.answer(texts.SUPPORT_OUTSIDE_HOURS)
            return await faq(message, user)
        if await support_service.has_reached_daily_limit(user.id):
            await message.answer(texts.SUPPORT_LIMIT_REACHED)
            return await faq(message, user)
        return await get_own_question(message, ex.context.get('topic'), user)
    # какая то хуйня, дай бог не произойдет
    except Exception as ex:
        logger.error(ex)
        await menu.start_message(message)
