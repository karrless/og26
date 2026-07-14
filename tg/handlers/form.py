from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from core.content import texts
from core.content.keyboards import Button, DIRECTIONS, YES_NO_KEYBOARD, CANCEL_KEYS
from core.content.texts import FORM_BUTTON, CANCEL_BUTTON
from core.keyboards import build_tg_keyboard
from core.pagination import Paginator
from core.services.form_service import FormValidationError, FormService, FormData
from core.services import SheetsService
from tg.states import FormStates
from tg.handlers import menu

router = Router()
form_service = FormService(SheetsService())

_DIRECTION_ENTRIES = list(DIRECTIONS.items())
NAV_PREV = "◀️ Назад"
NAV_NEXT = "Вперёд ▶️"


def _build_direction_page(page_num: int) -> tuple[ReplyKeyboardMarkup, int]:
    paginator = Paginator(_DIRECTION_ENTRIES, columns=1, reserved_rows=2)
    page = paginator.get_page(page_num)

    rows = [[Button(alias, alias)] for _, alias in page.items]

    nav_row = []
    if page.has_prev:
        nav_row.append(Button(NAV_PREV, NAV_PREV))
    if page.has_next:
        nav_row.append(Button(NAV_NEXT, NAV_NEXT))
    if nav_row:
        rows.append(nav_row)

    return build_tg_keyboard(rows, cancel=True), page.page


@router.message(StateFilter(FormStates), F.text == CANCEL_BUTTON)
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await menu.start_message(message, state)

@router.message(F.text.in_({FORM_BUTTON, "/form"}))
async def start_form(message: Message, state: FSMContext):
    await state.set_state(FormStates.fio)
    await message.answer(texts.FORM_ASK_FIO, reply_markup=build_tg_keyboard([CANCEL_KEYS]))


@router.message(FormStates.fio)
async def process_fio(message: Message, state: FSMContext):
    try:
        fio = form_service.validate_fio(message.text)
    except FormValidationError as e:
        return await message.answer(str(e))

    await state.update_data(fio=fio)
    await state.set_state(FormStates.vk_link)
    await message.answer(texts.FORM_ASK_VK, reply_markup=build_tg_keyboard([CANCEL_KEYS]))


@router.message(FormStates.vk_link)
async def process_vk_link(message: Message, state: FSMContext):
    vk_id = await form_service.validate_vk_link(message.text)
    if vk_id is None:
        return await message.answer(texts.FORM_VK_FAILED)

    await state.update_data(vk_id=vk_id)
    await state.set_state(FormStates.number)
    await message.answer(texts.FORM_ASK_NUMBER, reply_markup=build_tg_keyboard([CANCEL_KEYS]))


@router.message(FormStates.number)
async def process_number(message: Message, state: FSMContext):
    try:
        number = form_service.validate_unique_number(message.text)
    except FormValidationError as e:
        return await message.answer(str(e))

    await state.update_data(number=number)
    await state.set_state(FormStates.yes_no)
    await message.answer(texts.FORM_ASK_YES_NO, reply_markup=build_tg_keyboard(YES_NO_KEYBOARD), cancel=True)


@router.message(FormStates.yes_no)
async def process_yes_no(message: Message, state: FSMContext):
    try:
        yes_no = await form_service.validate_yes_no(message.text)
    except FormValidationError as e:
        return await message.answer(str(e))

    await state.update_data(yes_no=yes_no)
    await state.set_state(FormStates.direction)
    keyboard, page_num = _build_direction_page(1)
    await state.update_data(direction_page=page_num)
    await message.answer(texts.FORM_ASK_DIRECTION, reply_markup=keyboard)


@router.message(FormStates.direction)
async def process_direction(message: Message, state: FSMContext):
    data = await state.get_data()
    page_num = data.get("direction_page", 1)

    if message.text == NAV_PREV:
        keyboard, new_page = _build_direction_page(page_num - 1)
        await state.update_data(direction_page=new_page)
        return await message.answer(texts.FORM_ASK_DIRECTION, reply_markup=keyboard)

    if message.text == NAV_NEXT:
        keyboard, new_page = _build_direction_page(page_num + 1)
        await state.update_data(direction_page=new_page)
        return await message.answer(texts.FORM_ASK_DIRECTION, reply_markup=keyboard)

    direction = DIRECTIONS.get(message.text)
    if direction is None:
        return await message.answer(texts.FORM_NOT_FOUND)

    form_data = FormData(
        fio=data["fio"], vk_id=data["vk_id"], number=data["number"],
        yes_no=data["yes_no"], direction=direction,
    )
    ok = await form_service.submit(form_data)
    await state.clear()
    await message.answer(texts.FORM_DONE if ok else texts.FORM_NOT_FOUND)
    await menu.start_message(message, state)