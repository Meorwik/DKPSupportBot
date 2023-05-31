from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.default.default_keyboards import MenuKeyboardBuilder
from utils.db_api.connection_configs import ConnectionConfig
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.db_api import PostgresDataBaseManager
from utils.misc.logging import logging
from states.states import StateGroup
from aiogram import types
from loader import dp

greeting_message = """
Здравствуйте!
Я – бот, который поможет Вам оценить риск инфицирования ВИЧ и понять, нужны ли услуги по профилактике ВИЧ.
Для того чтобы продолжить, введите пожалуйста ваш УИК.

Если у вас нет УИКа, его можно составить по следующим инструкциям:
- Первые две буквы имени папы
- Первые две буквы имени мамы
- Ваш пол (1 - Мужчина, 2 - Женщина, 4 - Трансгендерная персона)
- Последние две цифры вашего года рождения.

Пример УИКа: ЕЛСА188
"""

empty_login_text = "Ваш профиль не имеет логина. Указать его можно в настройках.\nИнструкция:"
login_instruction_link = "https://inetfishki.ru/telegram/kak-uznat-dobavit-pomenyat-login.html#i-4"

async def is_valid_uik(uik: str):
    uik = uik.replace(" ", "")
    if uik[4: ].isnumeric() and len(uik) == 7:
        if uik[4] in "124":
            return True
        else:
            return False
    else:
        return False


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    if not message.from_user.username:
        empty_login_keyboard = InlineKeyboardMarkup()
        empty_login_fix_button = InlineKeyboardButton("Перейти", url=login_instruction_link)
        empty_login_keyboard.add(empty_login_fix_button)

        await message.answer(empty_login_text, reply_markup=empty_login_keyboard)

    else:
        postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())

        if await postgres_manager.check_user(message.from_user):
            await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))

        else:
            await message.answer(greeting_message)
            await StateGroup.in_uik.set()

@dp.message_handler(state=StateGroup.in_uik)
async def handle_uik(message: types.Message):
    if await is_valid_uik(message.text.lower()):
        postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
        await postgres_manager.add_user(message.from_user, uik=message.text)

        logging.info(f"Пользователь {message.from_user.id} успешно добавлен в базу!")
        user = await postgres_manager.get_user(user=message.from_user)
        await postgres_manager.database_log(user=user[0][0], action="Успешно добавлен в базу!")

        await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))

    else:
        await message.answer("Ошибка!\nПопробуйте снова.")
