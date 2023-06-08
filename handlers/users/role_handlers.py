from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder
from utils.db_api.connection_configs import ConnectionConfig
from utils.db_api.db_api import PostgresDataBaseManager
from data.config import ROLE_COMMANDS, ROLES, ROLE_NAMES
from aiogram.dispatcher import FSMContext
from states.states import StateGroup
from loader import dp, bot
from aiogram import types

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

message_for_consultant = """

От пациента
УИК: %uik
ID: %id
"""

def filter_consultant_commands(message: types.Message):
    if ROLE_COMMANDS["consultant_on"] == message.text:
        return True

    elif ROLE_COMMANDS["consultant_off"] == message.text:
        return True

    else:
        return False

@dp.message_handler(filter_consultant_commands, state="*")
async def handle_get_consult_role_command(message: types.Message, state: FSMContext):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())

    if message.text == ROLE_COMMANDS["consultant_on"]:
        await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["consultant"])
        await message.answer(greeting_consultant_message)
        await message.answer(consultant_instructions_message)
        await message.answer(reply_instruction)
        await StateGroup.in_consult.set()

    elif message.text == ROLE_COMMANDS["consultant_off"]:
        user_data = await postgres_manager.change_user_role(message.from_user, ROLE_NAMES["user"])
        await state.finish()
        await message.answer("Теперь вы не консультант!", reply_markup=SimpleKeyboardBuilder.get_back_to_menu_keyboard())

        if user_data["role"] != "user":
            await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["user"])
            await StateGroup.is_consultant.set()


@dp.message_handler(state=StateGroup.is_consultant)
async def handle_consultant_messages(message: types.Message):
    if message["reply_to_message"] is not None:
        # reply send to user
        pass


    else:
        await message.answer(consultant_instructions_message)
        await message.answer(reply_instruction)


@dp.message_handler(state=StateGroup.in_consult)
async def send_message_to_consultant(message: types.Message):
    consultants = ROLES["consultants"]
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    user_uik = await postgres_manager.get_user_uik(message.from_user)

    for i in consultants:
        await bot.send_message(text=message_for_consultant % (message.from_user.id, user_uik), chat_id=i)

