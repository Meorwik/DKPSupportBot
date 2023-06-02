from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    # Стэйты тестов
    in_hiv_risk_assessment = State()
    in_hiv_knowledge_assessment = State()
    in_pkp_assessment = State()
    in_sogi_assessment = State()
    in_understanding_PLHIV_assessment = State()

    # Другие стэйты
    in_uik = State()
