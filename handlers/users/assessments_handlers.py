from data.tests.test_manager import \
    TESTS_LANGUAGES_CALLBACKS, \
    HivRiskAssessment, \
    SogiAssessment, \
    HivKnowledgeAssessment, \
    PkpAssessment, \
    UnderstandingPLHIVAssessment
from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder, TestKeyboardBuilder
from utils.test_results_tamplate import TestResults
from aiogram.dispatcher import FSMContext
from loader import dp, postgres_manager
from utils.misc.logging import logging
from states.states import StateGroup
from datetime import datetime
from aiogram import types


# ---------------------------TESTS HANDLERS-----------------------------------------------

@dp.callback_query_handler(lambda call: call.data in TESTS_LANGUAGES_CALLBACKS, state=StateGroup.in_test)
async def handle_language_selection(call: types.CallbackQuery, state: FSMContext):
    test_keyboard_builder = TestKeyboardBuilder()
    database_data = TestResults()
    user = await postgres_manager.get_user(call.from_user.id)
    database_data.user_id = user["id"]

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
    await postgres_manager.database_log(database_data.user_id, f"Начал тест: {database_data.test_name}")
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

        await call.message.delete()
        database_data.datetime = f"{datetime.today().strftime('%d/%m/%Y')}"
        database_data = database_data.to_dict()
        await postgres_manager.add_new_test_results(database_data)
        logging.info(f"Пользователь {call.from_user.id} успешно завершил тест {database_data['test_name']}!")
        user = await postgres_manager.get_user(call.from_user.id)
        await postgres_manager.database_log(user['id'], action=f"Завершил тест {database_data['test_name']}!")

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
