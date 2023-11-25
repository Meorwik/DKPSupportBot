from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    in_test = State()
    in_uik = State()
    in_consult = State()


class RoleStates(StatesGroup):
    is_consultant = State()


class ReminderStates(StatesGroup):
    ...


class ReminderFillingForm(ReminderStates):
    in_drug_name = State()
    in_dose = State()
    in_time = State()


class RemindModify(ReminderStates):
    in_get_id = State()


class RemindDelete(ReminderStates):
    in_get_id = State()


class ReminderHistory(ReminderStates):
    in_history = State()