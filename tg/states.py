from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    fio = State()
    vk_link = State()
    number = State()
    yes_no = State()
    direction = State()