from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import is_admin

TESTS_BUTTONS_TEXTS = {
    "hiv_risk_assessment": "Оценка риска инфицирования ВИЧ 📋",
    "sogi_assessment": "Оценка знаний на тему СОГИ 📋",
    "pkp_assessment": "Тестирование ПКП 📋",
    "hiv_knowledge_assessment": "Оценка знаний о ВИЧ 📋",
    "understanding_PLHIV_assessment": "Тестирование на понимание ЛЖВ 📋",
}

INFO_BUTTONS_TEXTS = {
    "social_networks": "🔈 Мы в соц.сетях",
    "project_news": "📌 Новости проекта",
    "tell_partner": "🙋‍♀ Расскажите партнёру о важности тестирования анонимно",
    "info_files": "📚 Всё о доконтактной профилактике ВИЧ",
}

ADMIN_BUTTONS_TEXTS = {
    "get_users": "Получить базу пользователей",
}

MENU_BUTTONS_TEXTS = {
    "tests": "Тесты",
    "info": "Инфо",
    "admin": "⚙️ Панель администратора",
    "order_vih_test": "💊 Заказать бесплатный тест на ВИЧ",
    "contacting_consultant": "👤 Обращение к консультанту",
    "rate_bot": '✨ Оценить бота',
}

# КЛАСС: MenuKeyboardBuilder
# Создан для работы с клавиатурами, создает клавиатуры для меню и его разделов.
class MenuKeyboardBuilder:
    def __init__(self):
        self.__keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.__buttons = []

    def __add_admin_menu(self):
        admin_button = KeyboardButton(MENU_BUTTONS_TEXTS["admin"])
        self.__keyboard.add(admin_button)
        return True

    def __add_back_button(self):
        back_button = KeyboardButton("Назад в меню ⬅️")
        self.__keyboard.add(back_button)
    def get_main_menu_keyboard(self, user):
        self.__keyboard.clean()

        tests_button = KeyboardButton(MENU_BUTTONS_TEXTS["tests"])
        info_button = KeyboardButton(MENU_BUTTONS_TEXTS["info"])
        order_vih_test_button = KeyboardButton(MENU_BUTTONS_TEXTS["order_vih_test"])
        consult_button = KeyboardButton(MENU_BUTTONS_TEXTS["contacting_consultant"])
        rate_bot_button = KeyboardButton(MENU_BUTTONS_TEXTS["rate_bot"])

        self.__keyboard.row(tests_button,info_button)

        if is_admin(user):
            self.__add_admin_menu()

        self.__keyboard.add(order_vih_test_button, consult_button, rate_bot_button)

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
        self.__keyboard.clean()
        self.__keyboard.add(get_all_users_button)
        self.__add_back_button()
        return self.__keyboard

    def get_info_menu_keyboard(self):
        self.__keyboard.clean()
        social_networks_button = KeyboardButton(INFO_BUTTONS_TEXTS["social_networks"])
        project_news_button = KeyboardButton(INFO_BUTTONS_TEXTS["project_news"])
        tell_partner_button = KeyboardButton(INFO_BUTTONS_TEXTS["tell_partner"])
        info_files_button = KeyboardButton(INFO_BUTTONS_TEXTS["info_files"])

        self.__keyboard.add(social_networks_button, project_news_button, tell_partner_button, info_files_button)
        self.__add_back_button()

        return self.__keyboard
