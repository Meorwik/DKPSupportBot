from utils.db_api.connection_configs import ConnectionConfig
from utils.db_api.db_api import PostgresDataBaseManager
from data.config import ROLE_COMMANDS, ROLES, ROLE_NAMES
from aiogram.dispatcher import FSMContext
from states.states import StateGroup
from aiogram import types
from loader import dp

# --------------------------------------CONSULTANT ROLE HANDLERS -----------------------------------------------

greeting_consultant_message = """
Теперь вы стали консультантом !
"""

consultant_instructions_message = """
Инструкция: Ожидайте сообщений от пациентов. 

Чтобы ответить, делайте обязательно reply на сообщение, на которое хотите ответить. 
Тогда я смогу переслать его нужному пациенту. 
Чтобы перестать быть консультантом, напишите !&consultoff
"""

reply_instruction = """
Чтобы сделать reply, смахните сообщение пациента влево.
"""

def filter_consultant_role_commands(message: types.Message):
    if ROLE_COMMANDS["consultant_on"] in message.text:
        return True

    elif ROLE_COMMANDS["consultant_off"] in message.text:
        return True

    else:
        return False

@dp.message_handler(filter_consultant_role_commands, state="*")
async def handle_get_consult_role_command(message: types.Message, state: FSMContext):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    if ROLE_COMMANDS["consultant_on"]:
        await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["consultant"])
        await message.answer(greeting_consultant_message)
        await message.answer(consultant_instructions_message)
        await message.answer(reply_instruction)
        await StateGroup.in_consult.set()

    elif ROLE_COMMANDS["consultant_off"]:
        user_data = await postgres_manager.get_user(message.from_user)
        await state.finish()

        if user_data["role"] != "user":
            await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["user"])
            await StateGroup.in_consult.set()


@dp.message_handler(state=StateGroup.in_consult)
async def handle_consultant_messages(message: types.Message):
    if message["reply_to_message"] is not None:
        pass

    else:
        await message.answer(consultant_instructions_message)
        await message.answer(reply_instruction)