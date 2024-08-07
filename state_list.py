from aiogram.fsm.state import State, StatesGroup


class reserve_form(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    amount = State()
    date = State()
    time = State()
    confirm = State()