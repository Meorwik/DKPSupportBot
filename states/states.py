from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    in_test = State()
    in_uik = State()
