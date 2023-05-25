from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    in_hiv_risk_assessment = State()
    in_menu = State()
