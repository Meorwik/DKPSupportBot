from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.default.default_keyboards import MenuKeyboardBuilder
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot, postgres_manager
from aiogram.dispatcher import FSMContext
from utils.misc.logging import logging
from states.states import StateGroup
from datetime import datetime
from aiogram import types

greeting_message = """
Здравствуйте!

Я – бот, который поможет Вам оценить риск инфицирования ВИЧ и понять, нужны ли услуги по профилактике ВИЧ.
"""

uik_info = """
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


async def cancel_test_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return False

    else:
        try:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

            except MessageToDeleteNotFound:
                pass

            async with state.proxy() as state_memory:
                state_memory["data"].is_finished = False
                state_memory["data"].datetime = f"{datetime.today().strftime('%d/%m/%Y')}"
                state_memory["data"] = state_memory["data"].to_dict()
                await postgres_manager.add_new_test_results(state_memory["data"])

        except KeyError:
            pass

        await state.finish()
        await message.delete()

@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if not message.from_user.username:
        await state.finish()
        empty_login_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Перейти", url=login_instruction_link))
        await message.answer(text=empty_login_text, reply_markup=empty_login_keyboard)

    else:
        await cancel_test_handler(message, state)

        if not await postgres_manager.is_new_user(message.from_user):
            if await postgres_manager.get_user_uik(user=message.from_user) is not None:
                await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))

            else:
                await message.answer(uik_info)
                await StateGroup.in_uik.set()
        else:
            await message.answer(greeting_message)
            await message.answer(uik_info)
            await StateGroup.in_uik.set()

@dp.message_handler(state=StateGroup.in_uik)
async def handle_uik(message: types.Message, state: FSMContext):
    if await is_valid_uik(message.text.lower()):
        try:
            await postgres_manager.add_user(message.from_user, message.text)
        except:
            pass
        user = await postgres_manager.get_user(message.from_user.id)

        if user["uik"] is None:
            await postgres_manager.update_user_uik(message.from_user, uik=message.text)


        logging.info(f"Пользователь {message.from_user.id} успешно добавлен в базу!")
        await postgres_manager.database_log(user=user["id"], action="Успешно добавлен в базу!")

        await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))
        await state.finish()

    else:
        await message.answer("Ошибка!\nПопробуйте снова.")