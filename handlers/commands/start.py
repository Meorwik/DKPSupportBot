from utils.db_api.db_api import PostgresDataBaseManager
from utils.db_api.connection_configs import ConnectionConfig
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from loader import dp

greeting_message = """
Здравствуйте!
Я – бот, который поможет Вам оценить риск инфицирования ВИЧ и понять, нужны ли услуги по профилактике ВИЧ.
Нажмите "Начать!", чтобы продолжить:
"""

empty_login_text = "Ваш профиль не имеет логина. Указать его можно в настройках.\nИнструкция:"
login_instruction_link = "https://inetfishki.ru/telegram/kak-uznat-dobavit-pomenyat-login.html#i-4"


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    if not message.from_user.username:
        empty_login_keyboard = InlineKeyboardMarkup()
        empty_login_fix_button = InlineKeyboardButton("Перейти", url=login_instruction_link)
        empty_login_keyboard.add(empty_login_fix_button)

        await message.answer(empty_login_text, reply_markup=empty_login_keyboard)

    else:
        # postgres_manager = PostgresDataBaseManager(postgres_connection_config)
        # await postgres_manager.check_user(message.from_user)

        start_keyboard = InlineKeyboardMarkup(row_width=1)
        start_menu_button = InlineKeyboardButton("Начать!", callback_data="menu")
        start_keyboard.add(start_menu_button)

        await message.answer(greeting_message, reply_markup=start_keyboard)
