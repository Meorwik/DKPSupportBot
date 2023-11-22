from keyboards.default.default_keyboards import MENU_BUTTONS_TEXTS, MenuKeyboardBuilder, \
    TESTS_BUTTONS_TEXTS, ADMIN_BUTTONS_TEXTS, INFO_BUTTONS_TEXTS, BACK_BUTTONS_TEXTS, MEDICATION_SCHEDULE_BUTTONS_TEXTS
from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder, PeriodSelector, MEDICAL_SCHEDULE_BUTTON_MATERIALS
from states.states import StateGroup, ReminderFillingForm, RemindModify, RemindDelete, ReminderStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified
from utils.medical_schedule_tools import MedicalScheduleManager, Reminder
from utils.product_analytics import AnalyticsManager
from utils.medical_schedule_tools import Scheduler
from utils.forms_templates import SetReminder
from loader import dp, bot, postgres_manager
from aiogram.dispatcher import FSMContext
from utils.misc.logging import logging
from contextlib import suppress
from asyncio import sleep
from aiogram import types
import time


def is_time_format(arg):
    try:
        time.strptime(arg, '%H:%M')
        return True
    except ValueError:
        return False


# ----------------------------BACK BUTTONS HANDLERS---------------------------------
@dp.callback_query_handler(lambda call: call.data == "error")
async def handle_error_situation(callback: types.CallbackQuery):
    await callback.message.delete()
    logging.info(f"Пользователь {callback.from_user.id} получил ошибку!!!")
    await start_menu(callback)


@dp.message_handler(lambda message: message.text in BACK_BUTTONS_TEXTS.values())
async def handle_back_button(message: types.Message):
    if message.text == BACK_BUTTONS_TEXTS["back_to_menu"]:
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))


@dp.callback_query_handler(lambda callback: callback.data == 'menu')
async def start_menu(callback_query: types.CallbackQuery):
    with suppress(MessageToDeleteNotFound):
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id - 2)

    menu_keyboard = MenuKeyboardBuilder().get_main_menu_keyboard(callback_query.from_user)
    await callback_query.message.answer('Меню', reply_markup=menu_keyboard)
    await callback_query.message.delete()

# ------------------------------HANDLE MAIN MENU----------------------------------------------


@dp.message_handler(lambda message: message.text in MENU_BUTTONS_TEXTS.values())
async def handle_menu_buttons(message: types.Message):
    user = await postgres_manager.get_user(message.from_user.id)
    menu_keyboard_builder = MenuKeyboardBuilder()

    async def delete_past_messages(msg: types.Message):
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        await msg.delete()

    if message.text == MENU_BUTTONS_TEXTS["tests"]:
        await delete_past_messages(message)
        await message.answer("Меню тестов", reply_markup=menu_keyboard_builder.get_tests_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["info"]:
        await delete_past_messages(message)
        await message.answer("Меню информации", reply_markup=menu_keyboard_builder.get_info_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["admin"]:
        await delete_past_messages(message)
        await message.answer("Меню администратора", reply_markup=menu_keyboard_builder.get_admin_menu_keyboard())

    elif message.text == MENU_BUTTONS_TEXTS["order_vih_test"]:
        logging.info(f"Пользователь {message.from_user.id} Попытался заказать тест на ВИЧ!")
        await postgres_manager.add_log(user=user["id"], action="Попытался заказать тест на ВИЧ!")

        btn = InlineKeyboardButton("Перейти", url="https://hivtest.kz/")
        await message.answer('Заказать бесплатный тест', reply_markup=InlineKeyboardMarkup().add(btn))

    elif message.text == MENU_BUTTONS_TEXTS["contacting_consultant"]:
        logging.info(f"Пользователь {message.from_user.id} начал взаимодействие с консультантом!")
        await postgres_manager.add_log(user=user["id"], action="Начал взаимодействие с консультантом!")

        msg = await message.answer("Консультант подключается...", reply_markup=ReplyKeyboardRemove())
        await sleep(delay=1.2)
        await msg.delete()
        await message.answer("""
        Здравствуйте! Меня зовут Вильдамир. Готов ответить на Ваши вопросы.
        """, reply_markup=MenuKeyboardBuilder().get_end_conversation_keyboard())
        await StateGroup.in_consult.set()

    elif message.text == MENU_BUTTONS_TEXTS["medication_schedule"]:
        await delete_past_messages(message)

        medical_schedule_manager = MedicalScheduleManager()
        message_to_show = f"Активные напоминания:\n{await medical_schedule_manager.get_user_reminders_info(user['id'])}"

        users_registrations_count = await medical_schedule_manager.get_users_reminders_count(user["id"])
        await message.answer(
            text=message_to_show,
            reply_markup=menu_keyboard_builder.get_medication_schedule_keyboard(users_registrations_count),
            parse_mode=types.ParseMode.HTML
        )


# ------------------------------HANDLE ADMIN MENU----------------------------------------------

@dp.message_handler(lambda message: message.text in ADMIN_BUTTONS_TEXTS.values())
async def handle_admin_menu(message: types.Message):
    analytics_manager = AnalyticsManager()
    choose_month_text = "Выберите месяц:"

    if message.text == ADMIN_BUTTONS_TEXTS["get_users"]:
        saved_file_path = await postgres_manager.download_users_table()
        with open(saved_file_path, "rb") as users_data:
            await message.answer_document(users_data)

    elif message.text == ADMIN_BUTTONS_TEXTS["get_period_analytics"]:
        period_selector = PeriodSelector()
        keyboard = period_selector.get_keyboard()
        await message.answer(choose_month_text, reply_markup=keyboard)

    elif message.text == ADMIN_BUTTONS_TEXTS["get_all_analytics"]:
        msg = await message.answer("Идет анализ...\nЭто может занять некоторое время.")
        await analytics_manager.analyze_all()
        analytics = await analytics_manager.get_analytics_results()
        await msg.delete()
        await message.answer(analytics, "MARKDOWN")


@dp.callback_query_handler(lambda call: PeriodSelector.filter_callbacks(call))
async def handle_period_selection(call: types.CallbackQuery):
    period_selector = PeriodSelector()
    analytics_manager = AnalyticsManager()
    callback_components = period_selector.get_callback_components(call)

    if "[monthCallbacks]" in callback_components.values():
        await call.message.delete()
        msg = await call.message.answer("Идет анализ...\nЭто может занять некоторое время.")
        await analytics_manager.analyze_period(callback_components["date"])
        analytics = await analytics_manager.get_analytics_results()
        await msg.delete()
        await call.message.answer(analytics, "MARKDOWN")

    elif "[backCallback]" in callback_components.values():
        keyboard = period_selector.get_previous_year_keyboard(call)
        with suppress(MessageNotModified):
            await call.message.edit_reply_markup(keyboard)

    elif "[forwardCallback]" in callback_components.values():
        keyboard = period_selector.get_next_year_keyboard(call)
        with suppress(MessageNotModified):
            await call.message.edit_reply_markup(keyboard)


# ------------------------------HANDLE INFO MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in INFO_BUTTONS_TEXTS.values())
async def handle_info_menu(message: types.Message):
    user = await postgres_manager.get_user(message.from_user.id)

    visit_social_networks_text = "Facebook и Instagram страница проекта"
    project_news_text_1 = "О ВИЧ рассказывают подростки"
    project_news_text_2 = "Доконтактная профилактика: Новый способ профилактики ВИЧ в Казахстане"
    tell_your_partner_text = "Расскажите партнёру о важности тестирования анонимно 🙋‍♀"
    ask_language = "Выберите язык, чтобы продолжить:"
    about_developer_text = "Проконсультироваться или получить аудит можно в личных сообщениях👇"

    if message.text == INFO_BUTTONS_TEXTS["social_networks"]:
        keyboard = SimpleKeyboardBuilder.get_social_networks_keyboard()
        await message.answer(visit_social_networks_text, reply_markup=keyboard)

    elif message.text == INFO_BUTTONS_TEXTS["project_news"]:
        first_keyboard, second_keyboard = SimpleKeyboardBuilder.get_project_news_keyboards()
        await message.answer(project_news_text_1, reply_markup=first_keyboard)
        await message.answer(project_news_text_2, reply_markup=second_keyboard)

    elif message.text == INFO_BUTTONS_TEXTS["tell_partner"]:
        logging.info(f"Пользователь {message.from_user.id} рассказал партнеру о важности тестирования")
        await postgres_manager.add_log(user=user["id"], action="Рассказал партнеру о важности тестирования")
        keyboard = SimpleKeyboardBuilder.get_tell_partner_keyboard()
        await message.answer(tell_your_partner_text, reply_markup=keyboard)

    elif message.text == INFO_BUTTONS_TEXTS["info_files"]:
        keyboard = SimpleKeyboardBuilder.get_language_selection_documents_keyboard()
        await message.answer(ask_language, reply_markup=keyboard)

    elif message.text == INFO_BUTTONS_TEXTS["about_dev"]:
        with open("data/pictures/about_us.png", "rb") as picture:
            await message.answer_photo(
                photo=picture,
                caption=about_developer_text,
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    "Контактные данные 👨‍💻",
                    url="https://t.me/tyan_io")
                )
            )


# ------------------------------HANDLE TESTS MENU----------------------------------------------
@dp.message_handler(lambda message: message.text in TESTS_BUTTONS_TEXTS.values())
async def handle_tests_menu(message: types.Message):
    with suppress(MessageToDeleteNotFound):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

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


# ---------------------------------- HANDLE MEDICAL SCHEDULE MENU -----------------------------------------
@dp.message_handler(lambda message: message.text in MEDICATION_SCHEDULE_BUTTONS_TEXTS.values())
async def handle_medication_schedule(message: types.Message):

    if message.text == MEDICATION_SCHEDULE_BUTTONS_TEXTS["set_new_reminder"]:
        await message.answer("Введите название препарата:", reply_markup=MenuKeyboardBuilder().get_back_button_only())
        await ReminderFillingForm.in_drug_name.set()

    elif message.text == MEDICATION_SCHEDULE_BUTTONS_TEXTS["modify_reminder"]:
        await message.answer("Введите номер записи")
        await RemindModify.in_get_id.set()

    elif message.text == MEDICATION_SCHEDULE_BUTTONS_TEXTS["delete_reminder"]:
        await message.answer("Введите номер записи")
        await RemindDelete.in_get_id.set()


@dp.callback_query_handler(lambda call: call.data in MEDICAL_SCHEDULE_BUTTON_MATERIALS.keys())
async def handle_note_taking_medications(call: types.CallbackQuery):
    await call.answer("Записано ✅")
    await call.message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(call.from_user))
    await call.message.delete()


@dp.message_handler(lambda message: message.text in BACK_BUTTONS_TEXTS["back_to_menu"], state=ReminderStates)
async def handle_back_button(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Меню", reply_markup=MenuKeyboardBuilder().get_main_menu_keyboard(message.from_user))


@dp.message_handler(state=ReminderFillingForm.in_drug_name)
async def handle_reminder_set_drug_name(message: types.Message, state: FSMContext):
    reminder_form = SetReminder()
    reminder_form.drug_name = message.text

    async with state.proxy() as data:
        data["reminder_form"] = reminder_form

    await message.answer("Введите необходимую дозу препарата:")
    await state.set_state(ReminderFillingForm.in_dose)


@dp.message_handler(state=ReminderFillingForm.in_dose)
async def handle_reminder_set_drug_dose(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        reminder_form = data["reminder_form"]
        reminder_form.dose = message.text
        data["reminder_form"] = reminder_form

    format_warning = "Обратите внимание, формат вводимого времени должен быть примерно таким:\n\n12:40\n16:30\n21:02\n\nЧас : Минуты\nНикак иначе!"
    await message.answer("Введите время приема препарата:")
    await message.answer(format_warning)
    await state.set_state(ReminderFillingForm.in_time)


@dp.message_handler(state=ReminderFillingForm.in_time)
async def handle_reminder_set_drug_time(message: types.Message, state: FSMContext):
    if is_time_format(message.text):
        reminder_id = None
        async with state.proxy() as data:
            if "reminder_id" in data:
                if data["reminder_id"] is not None:
                    reminder_id = data["reminder_id"]

            reminder_form = data["reminder_form"]
            reminder_form.time = message.text
            data["reminder_form"] = reminder_form

        user = await postgres_manager.get_user(message.from_user.id)
        if reminder_id is None:
            await postgres_manager.add_medication_schedule_reminder(
                user["id"],
                reminder_form.drug_name,
                reminder_form.time, reminder_form.dose
            )

        else:
            await Scheduler().delete_reminder(reminder_id)
            await postgres_manager.modify_medication_schedule_reminder(
                reminder_id,
                user["id"],
                reminder_form.drug_name,
                reminder_form.dose,
                reminder_form.time
            )

        users_registrations_count = await MedicalScheduleManager().get_users_reminders_count(user["id"])

        await message.answer(
            text="Напоминание установлено !",
            reply_markup=MenuKeyboardBuilder().get_medication_schedule_keyboard(users_registrations_count)
        )

        user = await postgres_manager.get_user(message.from_user.id)
        await Scheduler().set_reminder(Reminder(
            user_id=user["id"],
            drug_name=reminder_form.drug_name,
            dose=reminder_form.dose,
            time=reminder_form.time,
        ), message)

        medical_schedule_manager = MedicalScheduleManager()
        message_to_show = f"Активные напоминания:\n{await medical_schedule_manager.get_user_reminders_info(user['id'])}"
        users_registrations_count = await medical_schedule_manager.get_users_reminders_count(user["id"])
        await message.answer(
            text=message_to_show,
            reply_markup=MenuKeyboardBuilder().get_medication_schedule_keyboard(users_registrations_count),
            parse_mode=types.ParseMode.HTML
        )

        await state.finish()

    else:
        format_warning = "Обратите внимание, формат вводимого времени должен быть примерно таким:\n\n12:40\n16:30\n21:02\n\nЧас : Минуты\nНикак иначе!"
        await message.answer(format_warning)
        await message.answer("Попробуйте еще раз!")


@dp.message_handler(state=RemindModify.in_get_id)
async def handle_get_id_to_modify(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        with suppress(ValueError):
            data["reminder_id"] = int(message.text)

    await message.answer("Введите название препарата:", reply_markup=MenuKeyboardBuilder().get_back_button_only())
    await state.set_state(ReminderFillingForm.in_drug_name)


@dp.message_handler(state=RemindDelete.in_get_id)
async def handle_get_id_to_delete(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        user = await postgres_manager.get_user(message.from_user.id)
        await postgres_manager.delete_medication_schedule_reminder(int(message.text), user["id"])
        await state.finish()

        medical_schedule_manager = MedicalScheduleManager()
        message_to_show = f"Активные напоминания:\n{await medical_schedule_manager.get_user_reminders_info(user['id'])}"
        users_registrations_count = await medical_schedule_manager.get_users_reminders_count(user["id"])
        await message.answer(
            text=message_to_show,
            reply_markup=MenuKeyboardBuilder().get_medication_schedule_keyboard(users_registrations_count),
            parse_mode=types.ParseMode.HTML
        )
        await Scheduler().delete_reminder(message.text)

    else:
        await message.answer("Ошибка!\nПопробуйте снова")

