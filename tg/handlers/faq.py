from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.content import texts
from core.content.texts import FAQ_BUTTON, CANCEL_BUTTON
from core.keyboards import build_tg_inline_keyboard
from core.pagination import Paginator, build_paginated_keyboard
from core.content.keyboards import Button
from core.services import FaqService
from tg.states import FaqStates
from tg.utils import reply, edit
from tg.handlers import menu

router = Router()
router.message.filter(F.chat.is_direct_messages == True)  # noqa: E712
router.callback_query.filter(F.message.chat.is_direct_messages == True)  # noqa: E712

faq_service = FaqService()


def _as_button_map(items, id_attr="id", title_attr="title") -> dict[str, str]:
    return {str(getattr(item, id_attr)): getattr(item, title_attr)[:40] for item in items}


@router.callback_query(F.data == "faq:start")
async def start_faq(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    topics = await faq_service.get_topics()
    if not topics:
        return await edit(callback, texts.FAQ_EMPTY)

    entries = list(_as_button_map(topics).items())
    await state.update_data(faq_topic_entries=entries, faq_topic_page=1)
    await state.set_state(FaqStates.topics)

    page = Paginator(entries, columns=2).get_page(1)
    rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"topic:pick:{e[0]}"), prefix="topic", columns=2)
    await edit(callback, texts.FAQ_ASK_TOPIC, reply_markup=build_tg_inline_keyboard(rows, cancel=True))


@router.callback_query(FaqStates.topics, F.data.startswith("topic:") | (F.data == "cancel"))
async def on_topic_action(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    await callback.answer()

    if action == "cancel":
        await state.clear()
        return await menu.start_message(callback.message, state)

    data = await state.get_data()
    entries = data["faq_topic_entries"]

    if action.startswith("topic:page:"):
        page_num = int(action.split(":")[-1])
        await state.update_data(faq_topic_page=page_num)
        page = Paginator(entries, columns=2).get_page(page_num)
        rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"topic:pick:{e[0]}"), prefix="topic", columns=2)
        return await edit(callback, texts.FAQ_ASK_TOPIC, reply_markup=build_tg_inline_keyboard(rows, cancel=True))

    if action.startswith("topic:pick:"):
        topic_id = int(action.split(":")[-1])
        topic = await faq_service.get_topic_full(topic_id)
        if topic is None:
            return await edit(callback, texts.FAQ_NOT_FOUND)

        text_parts = []

        if not topic.subtopics:
            text_parts.append(texts.FAQ_ASK_TOPIC)
            page = Paginator(entries, columns=2).get_page(data.get("faq_topic_page", 1))
            rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"topic:pick:{e[0]}"), prefix="topic", columns=2)
            return await edit(callback, "\n\n".join(text_parts), reply_markup=build_tg_inline_keyboard(rows, cancel=True))

        sub_entries = list(_as_button_map(topic.subtopics).items())
        subtopic_titles = [s.title for s in topic.subtopics]  # полные названия, без обрезки под 40 символов

        await state.update_data(
            faq_subtopic_entries=sub_entries,
            faq_subtopic_page=1,
            faq_current_topic_title=topic.title,
            faq_subtopic_titles=subtopic_titles,  # новое
        )
        await state.set_state(FaqStates.subtopics)

        page = Paginator(sub_entries, columns=2).get_page(1)
        rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"subtopic:pick:{e[0]}"), prefix="subtopic",
                                        columns=2)
        header = texts.FAQ_ASK_SUBTOPIC(topic.title, subtopic_titles)
        text_parts.append(header)
        text_parts.append(texts.TG_ASK_VK)
        await edit(callback, "\n\n".join(text_parts), reply_markup=build_tg_inline_keyboard(rows, back=True, cancel=True))


@router.callback_query(FaqStates.subtopics, F.data.startswith("subtopic:") | (F.data == "back") | (F.data == "cancel"))
async def on_subtopic_action(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    await callback.answer()

    if action == "cancel":
        await state.clear()
        return await menu.start_message(callback.message, state)

    data = await state.get_data()

    if action == "back":
        await state.set_state(FaqStates.topics)
        entries = data["faq_topic_entries"]
        page = Paginator(entries, columns=2).get_page(data.get("faq_topic_page", 1))
        rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"topic:pick:{e[0]}"), prefix="topic", columns=2)
        return await edit(callback, texts.FAQ_ASK_TOPIC, reply_markup=build_tg_inline_keyboard(rows, cancel=True))

    sub_entries = data["faq_subtopic_entries"]
    topic_title = data["faq_current_topic_title"]
    subtopic_titles = data["faq_subtopic_titles"]

    if action.startswith("subtopic:page:"):
        page_num = int(action.split(":")[-1])
        await state.update_data(faq_subtopic_page=page_num)
        page = Paginator(sub_entries, columns=2).get_page(page_num)
        rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"subtopic:pick:{e[0]}"), prefix="subtopic",
                                        columns=2)
        return await edit(
            callback, texts.FAQ_ASK_SUBTOPIC(topic_title, subtopic_titles),
            reply_markup=build_tg_inline_keyboard(rows, back=True, cancel=True),
        )

    if action.startswith("subtopic:pick:"):
        subtopic_id = int(action.split(":")[-1])
        subtopic = await faq_service.get_subtopic_full(subtopic_id)
        answer_text = subtopic.questions[0].answer if subtopic and subtopic.questions else texts.FAQ_NOT_FOUND

        page = Paginator(sub_entries, columns=2).get_page(data.get("faq_subtopic_page", 1))
        rows = build_paginated_keyboard(page, lambda e: Button(e[1], f"subtopic:pick:{e[0]}"), prefix="subtopic",
                                        columns=2)
        text = f"{answer_text}\n\n{texts.FAQ_ASK_SUBTOPIC(topic_title, subtopic_titles)}\n\n{texts.TG_ASK_VK}"
        return await edit(callback, text, reply_markup=build_tg_inline_keyboard(rows, back=True, cancel=True))