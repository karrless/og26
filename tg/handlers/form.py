from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.content import texts
from core.content.keyboards import Button, DIRECTIONS, YES_NO_KEYBOARD, CANCEL_KEYS
from core.keyboards import build_tg_inline_keyboard
from core.pagination import Paginator, build_paginated_keyboard
from core.services.form_service import FormValidationError, FormService, FormData
from core.services import SheetsService
from tg.states import FormStates
from tg.handlers import menu
from tg.utils import reply, edit, strip_keyboard

router = Router()
form_service = FormService(SheetsService())

# entry = (index, (full_name, alias)) — в callback_data кладём только index
_DIRECTION_ENTRIES = list(enumerate(sorted(DIRECTIONS.items(), key=lambda item: item[1])))


def _build_direction_rows(page):
    return build_paginated_keyboard(
        page,
        lambda entry: Button(entry[1][1], f"direction:pick:{entry[0]}"),  # entry[1][1] = alias, entry[0] = index
        prefix="direction", columns=1,
    )


async def _cancel_from_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await menu.start_message(callback.message, state)


@router.callback_query(F.data == "form:start")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(FormStates.fio)
    await edit(callback, texts.FORM_ASK_FIO, reply_markup=build_tg_inline_keyboard([CANCEL_KEYS]))
    await state.update_data(prompt_message_id=callback.message.message_id)


@router.callback_query(StateFilter(FormStates.fio, FormStates.vk_link, FormStates.number), F.data == "cancel")
async def cancel_during_text_step(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _cancel_from_callback(callback, state)


@router.message(FormStates.fio)
async def process_fio(message: Message, state: FSMContext):
    try:
        fio = form_service.validate_fio(message.text)
    except FormValidationError as e:
        return await message.answer(str(e))

    data = await state.get_data()
    await strip_keyboard(message, data["prompt_message_id"])

    await state.update_data(fio=fio)
    await state.set_state(FormStates.vk_link)
    prompt = await reply(message, texts.FORM_ASK_VK, reply_markup=build_tg_inline_keyboard([CANCEL_KEYS]))
    await state.update_data(prompt_message_id=prompt.message_id)


@router.message(FormStates.vk_link)
async def process_vk_link(message: Message, state: FSMContext):
    try:
        vk_id = await form_service.validate_vk_link(message.text)
        if vk_id is None:
            return await message.answer(texts.FORM_VK_FAILED)
    except FormValidationError as e:
        return await message.answer(str(e))

    data = await state.get_data()
    await strip_keyboard(message, data["prompt_message_id"])

    await state.update_data(vk_id=vk_id)
    await state.set_state(FormStates.number)
    prompt = await reply(message, texts.FORM_ASK_NUMBER, reply_markup=build_tg_inline_keyboard([CANCEL_KEYS]))
    await state.update_data(prompt_message_id=prompt.message_id)


@router.message(FormStates.number)
async def process_number(message: Message, state: FSMContext):
    try:
        number = form_service.validate_unique_number(message.text)
    except FormValidationError as e:
        return await message.answer(str(e))

    data = await state.get_data()
    await strip_keyboard(message, data["prompt_message_id"])

    await state.update_data(number=number)
    await state.set_state(FormStates.yes_no)
    prompt = await reply(
        message, texts.FORM_ASK_YES_NO,
        reply_markup=build_tg_inline_keyboard(YES_NO_KEYBOARD, cancel=True),
    )
    await state.update_data(prompt_message_id=prompt.message_id)


@router.callback_query(StateFilter(FormStates.yes_no), F.data.startswith("form:yes_no:") | (F.data == "cancel"))
async def on_yes_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "cancel":
        return await _cancel_from_callback(callback, state)

    yes_no = callback.data.split(":")[-1]
    await state.update_data(yes_no=yes_no)
    await state.set_state(FormStates.direction)
    await state.update_data(direction_page=1)

    page = Paginator(_DIRECTION_ENTRIES, columns=1).get_page(1)
    rows = _build_direction_rows(page)
    await edit(callback, texts.FORM_ASK_DIRECTION, reply_markup=build_tg_inline_keyboard(rows, cancel=True))


@router.callback_query(StateFilter(FormStates.direction), F.data.startswith("direction:") | (F.data == "cancel"))
async def on_direction(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "cancel":
        return await _cancel_from_callback(callback, state)

    if callback.data.startswith("direction:page:"):
        page_num = int(callback.data.split(":")[-1])
        await state.update_data(direction_page=page_num)
        page = Paginator(_DIRECTION_ENTRIES, columns=1).get_page(page_num)
        rows = _build_direction_rows(page)
        return await edit(callback, texts.FORM_ASK_DIRECTION, reply_markup=build_tg_inline_keyboard(rows, cancel=True))

    # direction:pick:<index>
    index = int(callback.data.split(":")[-1])
    direction = _DIRECTION_ENTRIES[index][1][0]  # [1] = (full, alias), [0] = full

    data = await state.get_data()
    form_data = FormData(
        fio=data["fio"], vk_id=data["vk_id"], number=data["number"],
        yes_no=data["yes_no"], direction=direction,
    )
    ok = await form_service.submit(form_data)
    await state.clear()
    await edit(callback, texts.FORM_DONE if ok else texts.FORM_NOT_FOUND)
    await menu.start_message(callback.message, state)