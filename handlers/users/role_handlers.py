from data.config import ROLE_COMMANDS, ROLES, ROLE_NAMES
from aiogram import types
from loader import dp

def filter_consultant_role_commands(message: types.Message):
    if ROLE_COMMANDS["consultant_on"] in message.text:
        return True

    elif ROLE_COMMANDS["consultant_off"] in message.text:
        return True

    else:
        return False

@dp.message_handler(filter_consultant_role_commands, state="*")
async def handle_get_consult_role_command(message: types.Message):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    if ROLE_COMMANDS["consultant_on"]:
        await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["consultant"])

    elif ROLE_COMMANDS["consultant_off"]:
        user_data = await postgres_manager.get_user(message.from_user)

        if user_data["role"] != "user":
            await postgres_manager.change_user_role(user=message.from_user, new_role=ROLE_NAMES["user"])

