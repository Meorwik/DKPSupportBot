from data.assessments.assessments_manager import ASSESSMENTS_NAMES
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import ROLE_COMMANDS
from data.config import is_admin

TESTS_BUTTONS_TEXTS = ASSESSMENTS_NAMES

INFO_BUTTONS_TEXTS = {
    "social_networks": "🔈 Мы в соц.сетях",
    "project_news": "📌 Новости проекта",
    "tell_partner": "🙋‍♀ Расскажите партнёру о важности тестирования анонимно",
    "info_files": "📚 Всё о доконтактной профилактике ВИЧ",
    "about_dev": "🔍 О разработчике"
}

ADMIN_BUTTONS_TEXTS = {
    "get_users": "Получить базу пользователей",
    "get_period_analytics": "Аналитика за период",
    "get_all_analytics": "Общая аналитика",
    "create_newsletter": "Создать рассылку"
}

MENU_BUTTONS_TEXTS = {
    "tests": "Тесты",
    "info": "Инфо",
    "admin": "⚙️ Панель администратора",
    "order_vih_test": "💊 Заказать бесплатный тест на ВИЧ",
    "contacting_consultant": "👤 Обращение к консультанту",
    "medication_schedule": "📖 Настроить напоминания приема препаратов",
    "rate_bot": '✨ Оценить бота',
}


BACK_BUTTONS_TEXTS = {
    "back_to_menu": "Назад в меню ⬅️",
    "end_conversation": "Закончить общение"
}


MEDICATION_SCHEDULE_BUTTONS_TEXTS = {
    "set_new_reminder": "⏰ Настроить новое напоминание",
    "get_reminders_history": "📜 Посмотреть историю отмеченных напоминаний",
    "modify_reminder": "🛠 Настроить активные напоминания",
    "delete_reminder": "❌ Удалить напоминание",
}


# КЛАСС: MenuKeyboardBuilder
# Создан для работы с клавиатурами, создает клавиатуры для меню и его разделов.
class MenuKeyboardBuilder:
    def __init__(self):
        self.__keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    def __add_admin_menu(self):
        admin_button = KeyboardButton(MENU_BUTTONS_TEXTS["admin"])
        self.__keyboard.add(admin_button)
        return True

    def __add_back_button(self):
        back_button = KeyboardButton(BACK_BUTTONS_TEXTS["back_to_menu"])
        self.__keyboard.add(back_button)

    def get_main_menu_keyboard(self, user):
        self.__keyboard.clean()

        tests_button = KeyboardButton(MENU_BUTTONS_TEXTS["tests"])
        info_button = KeyboardButton(MENU_BUTTONS_TEXTS["info"])
        order_vih_test_button = KeyboardButton(MENU_BUTTONS_TEXTS["order_vih_test"])
        consult_button = KeyboardButton(MENU_BUTTONS_TEXTS["contacting_consultant"])
        medication_schedule = KeyboardButton(MENU_BUTTONS_TEXTS["medication_schedule"])

        self.__keyboard.row(tests_button, info_button)

        if is_admin(user):
            self.__add_admin_menu()

        self.__keyboard.add(order_vih_test_button, consult_button, medication_schedule)

        return self.__keyboard

    def get_tests_menu_keyboard(self):
        hiv_risk_assessment_button = KeyboardButton(TESTS_BUTTONS_TEXTS["hiv_risk_assessment"])
        sogi_assessment_button = KeyboardButton(TESTS_BUTTONS_TEXTS["sogi_assessment"])
        pkp_assessment_button = KeyboardButton(TESTS_BUTTONS_TEXTS["pkp_assessment"])
        hiv_knowledge_assessment_button = KeyboardButton(TESTS_BUTTONS_TEXTS["hiv_knowledge_assessment"])
        understanding_PLHIV_assessment_button = KeyboardButton(TESTS_BUTTONS_TEXTS["understanding_PLHIV_assessment"])

        self.__keyboard.clean()
        self.__keyboard.add(
            hiv_risk_assessment_button,
            sogi_assessment_button,
            pkp_assessment_button,
            hiv_knowledge_assessment_button,
            understanding_PLHIV_assessment_button
        )

        self.__add_back_button()
        return self.__keyboard

    def get_admin_menu_keyboard(self):
        get_all_users_button = KeyboardButton(ADMIN_BUTTONS_TEXTS["get_users"])
        get_period_analytics_button = KeyboardButton(ADMIN_BUTTONS_TEXTS["get_period_analytics"])
        get_common_analytics_button = KeyboardButton(ADMIN_BUTTONS_TEXTS["get_all_analytics"])
        create_newsletter = KeyboardButton(ADMIN_BUTTONS_TEXTS["create_newsletter"])

        self.__keyboard.clean()
        self.__keyboard.add(
            get_all_users_button,
            create_newsletter,
            get_period_analytics_button,
            get_common_analytics_button
        )
        self.__add_back_button()
        return self.__keyboard

    def get_info_menu_keyboard(self):
        self.__keyboard.clean()
        social_networks_button = KeyboardButton(INFO_BUTTONS_TEXTS["social_networks"])
        project_news_button = KeyboardButton(INFO_BUTTONS_TEXTS["project_news"])
        tell_partner_button = KeyboardButton(INFO_BUTTONS_TEXTS["tell_partner"])
        info_files_button = KeyboardButton(INFO_BUTTONS_TEXTS["info_files"])
        about_dev = KeyboardButton(INFO_BUTTONS_TEXTS["about_dev"])

        self.__keyboard.add(
            social_networks_button,
            project_news_button,
            tell_partner_button,
            info_files_button,
            about_dev
        )
        self.__add_back_button()

        return self.__keyboard

    def get_back_button_only(self):
        self.__add_back_button()
        return self.__keyboard

    def get_consultant_menu(self):
        self.__keyboard.clean()
        consult_off_button = KeyboardButton(ROLE_COMMANDS["consultant_off"])
        self.__keyboard.add(consult_off_button)
        return self.__keyboard

    def get_end_conversation_keyboard(self):
        self.__keyboard.clean()
        end_conversation_button = KeyboardButton(BACK_BUTTONS_TEXTS["end_conversation"])
        return self.__keyboard.add(end_conversation_button)

    def get_medication_schedule_keyboard(self, registrations_count):
        self.__keyboard.clean()
        set_new_reminder = KeyboardButton(MEDICATION_SCHEDULE_BUTTONS_TEXTS["set_new_reminder"])
        self.__keyboard.add(set_new_reminder)

        if registrations_count > 0:
            reminders_history = KeyboardButton(MEDICATION_SCHEDULE_BUTTONS_TEXTS["get_reminders_history"])
            modify_reminder = KeyboardButton(MEDICATION_SCHEDULE_BUTTONS_TEXTS["modify_reminder"])
            delete_reminder = KeyboardButton(MEDICATION_SCHEDULE_BUTTONS_TEXTS["delete_reminder"])
            self.__keyboard.add(reminders_history, modify_reminder, delete_reminder)

        self.__add_back_button()
        return self.__keyboard

