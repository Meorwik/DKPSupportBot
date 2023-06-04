from keyboards.default.default_keyboards import \
    MENU_BUTTONS_TEXTS, \
    MenuKeyboardBuilder, \
    TESTS_BUTTONS_TEXTS, \
    ADMIN_BUTTONS_TEXTS, \
    INFO_BUTTONS_TEXTS
from data.tests.test_manager import \
    TESTS_LANGUAGES_CALLBACKS, \
    HivRiskAssessment, \
    SogiAssessment, \
    HivKnowledgeAssessment, \
    PkpAssessment, \
    UnderstandingPLHIVAssessment
from utils.db_api.db_api import PostgresDataBaseManager, DataConvertor, DB_USERS_COLUMNS
from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder, TestKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from utils.db_api.connection_configs import ConnectionConfig
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.test_results_tamplate import TestResults
from aiogram.dispatcher import FSMContext
from utils.misc.logging import logging
from states.states import StateGroup
from datetime import datetime
from loader import dp, bot
from aiogram import types


from aiogram.dispatcher.filters import Text
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
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())
    user = await postgres_manager.get_user(user=callback_query.from_user)
    await postgres_manager.database_log(user=user[0][0], action="Начал взаимодействие с ботом!")
    logging.info(f"Пользователь {callback_query.from_user.id} начал взаимодействие с ботом!")
    await callback_query.message.delete()

# ------------------------------HANDLE MAIN MENU----------------------------------------------

@dp.message_handler(lambda message: message.text in MENU_BUTTONS_TEXTS.values())
async def handle_menu_buttons(message: types.Message):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())
    user = await postgres_manager.get_user(user=message.from_user)

    if message.text == MENU_BUTTONS_TEXTS["tests"]:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await message.delete()
        await message.answer("Меню тестов", reply_markup=MenuKeyboardBuilder().get_tests_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["info"]:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await message.delete()
        await message.answer("Меню информации", reply_markup=MenuKeyboardBuilder().get_info_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["admin"]:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await message.delete()
        await message.answer("Меню администратора", reply_markup=MenuKeyboardBuilder().get_admin_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["order_vih_test"]:
        # Это все равно временный вариант, до того как мы не сделаем работу с API
        logging.info(f"Пользователь {message.from_user.id} Попытался заказать тест на ВИЧ!")
        await postgres_manager.database_log(user=user[0][0], action="Попытался заказать тест на ВИЧ!")

        btn = InlineKeyboardButton("Перейти", url="https://hivtest.kz/")
        await message.answer('Заказать бесплатный тест', reply_markup=InlineKeyboardMarkup().add(btn))

    elif message.text == MENU_BUTTONS_TEXTS["rate_bot"]:
        await message.answer("Еще в процессе разработки...")

    elif message.text == MENU_BUTTONS_TEXTS["contacting_consultant"]:
        logging.info(f"Пользователь {message.from_user.id} начал взаимодействие с консультантом!")
        await postgres_manager.database_log(user=user[0][0], action="Начал взаимодействие с консультантом!")

# ------------------------------HANDLE ADMIN MENU----------------------------------------------

@dp.message_handler(lambda message: message.text in ADMIN_BUTTONS_TEXTS.values())
async def handle_admin_menu(message: types.Message):
    if message.text == ADMIN_BUTTONS_TEXTS["get_users"]:
        postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())
        saved_file_path = await postgres_manager.download_users_table()

        with open(saved_file_path, "rb") as users_data:
            await bot.send_document(chat_id=message.from_user.id, document=users_data)

# ------------------------------HANDLE INFO MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in INFO_BUTTONS_TEXTS.values())
async def handle_info_menu(message: types.Message):
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())
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
        await postgres_manager.database_log(user=user[0][0], action="Рассказал партнеру о важности тестирования")

        product = SimpleKeyboardBuilder.get_tell_partner_keyboard()
        await message.answer(text=product["text"], reply_markup=product["keyboard"])

    elif message.text == INFO_BUTTONS_TEXTS["info_files"]:
        product = SimpleKeyboardBuilder.get_language_selection_documents_keyboard()
        await message.answer(text=product["text"], reply_markup=product["keyboard"])

@dp.callback_query_handler(lambda call: call.data == "send_document_KZ" or call.data == 'send_document_RU')
async def send_info_document(callback_query: types.CallbackQuery):
    if callback_query.data == "send_document_RU":
        await callback_query.message.edit_text("Пару секунд, загружаю информацию...")

        with open("data/info_files/Что такое ДКП ВИЧ.pdf", "rb") as ru_document:
            await callback_query.message.answer_document(ru_document)

    elif callback_query.data == "send_document_KZ":
        await callback_query.message.edit_text("Бірнеше секунд, ақпаратты жүктеп салу...")

        with open("data/info_files/КДП дегеніміз не.pdf", "rb") as kz_document:
            await callback_query.message.answer_document(kz_document)

    await callback_query.message.delete()
# ------------------------------HANDLE TESTS MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in TESTS_BUTTONS_TEXTS.values())
async def handle_tests_menu(message: types.Message):
    msg = await message.answer("Меню скрыто!", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

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
# ---------------------------TESTS HANDLERS-----------------------------------------------

@dp.callback_query_handler(lambda call: call.data in TESTS_LANGUAGES_CALLBACKS, state=StateGroup.in_test)
async def handle_language_selection(call: types.CallbackQuery, state: FSMContext):
    test_keyboard_builder = TestKeyboardBuilder()
    database_data = TestResults()
    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())
    user = await postgres_manager.get_user(call.from_user)
    database_data.user_id = user[0][0]

    if "hiv_risk_assessment" in call.data:
        database_data.test_name = 'hiv_risk_assessment'
        assessment = HivRiskAssessment()

    elif "sogi_assessment" in call.data:
        database_data.test_name = 'sogi_assessment'
        assessment = SogiAssessment()

    elif "pkp_assessment" in call.data:
        database_data.test_name = 'pkp_assessment'
        assessment = PkpAssessment()

    elif "hiv_knowledge_assessment" in call.data:
        database_data.test_name = 'hiv_knowledge_assessment'
        assessment = HivKnowledgeAssessment()

    else:
        database_data.test_name = 'understanding_PLHIV_assessment'
        assessment = UnderstandingPLHIVAssessment()

    logging.info(f"Пользователь {call.from_user.id} начал тест: {database_data.test_name}")
    await postgres_manager.database_log(user[0][0], f"Начал тест: {database_data.test_name}")
    del postgres_manager

    if call.data.startswith("ru"):
        database_data.language = 'ru'
        test_materials = assessment.get_ru_version()

    elif call.data.startswith("kz"):
        database_data.language = 'kz'
        test_materials = assessment.get_kz_version()

    else:
        database_data.language = 'ru'
        test_materials = assessment.get_ru_version()

    keyboards = test_keyboard_builder.get_keyboards(test_materials=test_materials)
    async with state.proxy() as state_memory:
        state_memory["keyboards"] = keyboards
        state_memory['score'] = 0
        state_memory["question_number"] = 1
        state_memory["results"] = test_materials["result_ratings"]
        state_memory["data"] = database_data

    await call.message.answer(keyboards["question_1"]["text"], reply_markup=keyboards["question_1"]["keyboard"])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await call.message.delete()



async def handle_tests_callbacks(state: FSMContext, call: types.CallbackQuery, max_result, min_result, medium_result_min, medium_result_max):
    async with state.proxy() as state_memory:
        state_memory["score"] += int(call.data)
        state_memory["question_number"] += 1
        score = state_memory["score"]
        keyboards = state_memory["keyboards"]
        question_number = state_memory["question_number"]
        results = state_memory["results"]
        database_data = state_memory["data"]

    postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_test_db_connection_config())

    high_risk = results["high"]
    medium_risk = results["medium"]
    small_risk = results['small']

    if question_number == len(keyboards):
        database_data.is_finished = True
        await state.finish()
        back_to_menu = SimpleKeyboardBuilder.get_back_to_menu_keyboard()

        if score >= max_result:
            await call.message.answer(text=high_risk, reply_markup=back_to_menu)
            database_data.result = 'high_result'

        elif medium_result_max >= score >= medium_result_min:
            await call.message.answer(text=medium_risk, reply_markup=back_to_menu)
            database_data.result = 'medium_result'

        elif score <= min_result:
            await call.message.answer(text=small_risk, reply_markup=back_to_menu)
            database_data.result = 'small_result'

        database_data.datetime = f"{datetime.today().strftime('%d/%m/%Y')}"
        database_data = database_data.to_dict()
        await postgres_manager.add_new_test_results(database_data)
        logging.info(f"Пользователь {call.from_user.id} успешно завершил тест {database_data['test_name']}!")
        user = await postgres_manager.get_user(user=call.from_user)
        await postgres_manager.database_log(user[0][0], action=f"Успешно завершил тест {database_data['test_name']}!")

    else:
        await call.message.edit_text\
            (
                text=keyboards[f"question_{question_number}"]["text"],
                reply_markup=keyboards[f"question_{question_number}"]["keyboard"]
            )

@dp.callback_query_handler(state=StateGroup.in_test)
async def handle_hiv_risk_assessment(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as state_memory:
        test_name = state_memory["data"].test_name

    if test_name == "hiv_risk_assessment":
        await handle_tests_callbacks(state, call,
                                     max_result=22,
                                     min_result=7,
                                     medium_result_min=7,
                                     medium_result_max=21)

    elif test_name == "sogi_assessment":
        await handle_tests_callbacks(state, call,
                                     max_result=17,
                                     min_result=9,
                                     medium_result_max=16,
                                     medium_result_min=10)

    elif test_name == "pkp_assessment":
        await handle_tests_callbacks(state, call,
                                     max_result=8,
                                     min_result=3,
                                     medium_result_max=7,
                                     medium_result_min=4)

    elif test_name == "hiv_knowledge_assessment":
        await handle_tests_callbacks(state, call,
                                     max_result=13,
                                     min_result=6,
                                     medium_result_max=12,
                                     medium_result_min=7)

    elif test_name == "understanding_PLHIV_assessment":
        await handle_tests_callbacks(state, call,
                                     max_result=11,
                                     min_result=5,
                                     medium_result_max=10,
                                     medium_result_min=6)
