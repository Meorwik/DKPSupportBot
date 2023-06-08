from keyboards.default.default_keyboards import MENU_BUTTONS_TEXTS, MenuKeyboardBuilder, \
    TESTS_BUTTONS_TEXTS, ADMIN_BUTTONS_TEXTS, INFO_BUTTONS_TEXTS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder
from utils.db_api.connection_configs import ConnectionConfig
from aiogram.utils.exceptions import MessageToDeleteNotFound
from utils.db_api.db_api import PostgresDataBaseManager
from utils.misc.logging import logging
from states.states import StateGroup
from contextlib import suppress
from loader import dp, bot
from asyncio import sleep
from aiogram import types


# ----------------------------BACK BUTTONS HANDLERS---------------------------------
@dp.callback_query_handler(lambda call: call.data == "error")
async def handle_error_situation(callback: types.CallbackQuery):
    await callback.message.delete()
    logging.info(f"Пользователь {call.from_user.id} получил ошибку!!!!!!!")

@dp.message_handler(lambda message: message.text == "Назад в меню ⬅️")
async def handle_back_button(message: types.Message):
    if message.text == "Назад в меню ⬅️":
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))

@dp.callback_query_handler(lambda callback: callback.data == 'menu')
async def start_menu(callback_query: types.CallbackQuery):
    menu_keyboard = MenuKeyboardBuilder().get_main_menu_keyboard(callback_query.from_user)
    await callback_query.message.answer('Меню', reply_markup=menu_keyboard)
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    user = await postgres_manager.get_user(user=callback_query.from_user)
    await postgres_manager.database_log(user=user["id"], action="Начал взаимодействие с ботом!")
    logging.info(f"Пользователь {callback_query.from_user.id} начал взаимодействие с ботом!")
    await callback_query.message.delete()

# ------------------------------HANDLE MAIN MENU----------------------------------------------

@dp.message_handler(lambda message: message.text in MENU_BUTTONS_TEXTS.values())
async def handle_menu_buttons(message: types.Message):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    user = await postgres_manager.get_user(user=message.from_user)

    async def delete_past_messages(msg: types.Message):
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        await msg.delete()

    if message.text == MENU_BUTTONS_TEXTS["tests"]:
        await delete_past_messages(message)
        await message.answer("Меню тестов", reply_markup=MenuKeyboardBuilder().get_tests_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["info"]:
        await delete_past_messages(message)
        await message.answer("Меню информации", reply_markup=MenuKeyboardBuilder().get_info_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["admin"]:
        await delete_past_messages(message)
        await message.answer("Меню администратора", reply_markup=MenuKeyboardBuilder().get_admin_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["order_vih_test"]:
        logging.info(f"Пользователь {message.from_user.id} Попытался заказать тест на ВИЧ!")
        await postgres_manager.database_log(user=user["id"], action="Попытался заказать тест на ВИЧ!")

        btn = InlineKeyboardButton("Перейти", url="https://hivtest.kz/")
        await message.answer('Заказать бесплатный тест', reply_markup=InlineKeyboardMarkup().add(btn))

    elif message.text == MENU_BUTTONS_TEXTS["rate_bot"]:
        await message.answer("Еще в процессе разработки...")

    elif message.text == MENU_BUTTONS_TEXTS["contacting_consultant"]:
        logging.info(f"Пользователь {message.from_user.id} начал взаимодействие с консультантом!")
        await postgres_manager.database_log(user=user["id"], action="Начал взаимодействие с консультантом!")

        msg = await message.answer("Консультант подключается...", reply_markup=ReplyKeyboardRemove())
        await sleep(delay=1.2)
        await msg.delete()
        await message.answer("""
        Здравствуйте! Меня зовут Михаил. Готов ответить на Ваши вопросы.
        """)
        await StateGroup.in_consult.set()

# ------------------------------HANDLE ADMIN MENU----------------------------------------------

@dp.message_handler(lambda message: message.text in ADMIN_BUTTONS_TEXTS.values())
async def handle_admin_menu(message: types.Message):
    if message.text == ADMIN_BUTTONS_TEXTS["get_users"]:
        postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
        saved_file_path = await postgres_manager.download_users_table()

        with open(saved_file_path, "rb") as users_data:
            await bot.send_document(chat_id=message.from_user.id, document=users_data)

# ------------------------------HANDLE INFO MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in INFO_BUTTONS_TEXTS.values())
async def handle_info_menu(message: types.Message):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
    user = await postgres_manager.get_user(user=message.from_user)

    if message.text == INFO_BUTTONS_TEXTS["social_networks"]:
        product = SimpleKeyboardBuilder.get_social_networks_keyboard()
        await message.answer(text=product["text"], reply_markup=product["keyboard"])

    elif message.text == INFO_BUTTONS_TEXTS["project_news"]:
        product = SimpleKeyboardBuilder.get_project_news_keyboards()
        await message.answer(text=product[0]["text"], reply_markup=product[0]["keyboard"])
        await message.answer(text=product[1]["text"], reply_markup=product[1]["keyboard"])

    elif message.text == INFO_BUTTONS_TEXTS["tell_partner"]:
        logging.info(f"Пользователь {message.from_user.id} рассказал партнеру о важности тестирования")
        await postgres_manager.database_log(user=user["id"], action="Рассказал партнеру о важности тестирования")

        product = SimpleKeyboardBuilder.get_tell_partner_keyboard()
        await message.answer(text=product["text"], reply_markup=product["keyboard"])

    elif message.text == INFO_BUTTONS_TEXTS["info_files"]:
        product = SimpleKeyboardBuilder.get_language_selection_documents_keyboard()
        await message.answer(text=product["text"], reply_markup=product["keyboard"])

# ------------------------------HANDLE TESTS MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in TESTS_BUTTONS_TEXTS.values())
async def handle_tests_menu(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

    except:
        pass
    await message.delete()

    choose_language_text = "Выберите язык, чтобы продолжить:"

    if message.text == TESTS_BUTTONS_TEXTS["hiv_risk_assessment"]:
        language_select_keyboard = SimpleKeyboardBuilder.get_language_selection_keyboard("hiv_risk_assessment")

    elif message.text == TESTS_BUTTONS_TEXTS["hiv_knowledge_assessment"]:
        language_select_keyboard = SimpleKeyboardBuilder.get_language_selection_keyboard("hiv_knowledge_assessment")

    elif message.text == TESTS_BUTTONS_TEXTS["sogi_assessment"]:
        language_select_keyboard = SimpleKeyboardBuilder.get_language_selection_keyboard("sogi_assessment")

    elif message.text == TESTS_BUTTONS_TEXTS["pkp_assessment"]:
        language_select_keyboard = SimpleKeyboardBuilder.get_language_selection_keyboard("pkp_assessment")

    elif message.text == TESTS_BUTTONS_TEXTS["understanding_PLHIV_assessment"]:
        language_select_keyboard = SimpleKeyboardBuilder.get_language_selection_keyboard("understanding_PLHIV_assessment")

    else:
        language_select_keyboard = SimpleKeyboardBuilder.get_error_keyboard()

    await message.answer(
        text=choose_language_text,
        reply_markup=language_select_keyboard
    )
    await StateGroup.in_test.set()

