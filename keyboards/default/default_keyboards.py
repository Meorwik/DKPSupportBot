from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import is_admin

MENU_BUTTONS_TEXTS = {
    "hiv_risk_assessment": "Тест на оценку риска инфицирования ВИЧ 📋",
    "info_files": "Всё о доконтактной профилактике ВИЧ 📚",
    "order_vih_test": "Заказать бесплатный тест на ВИЧ 💊",
    "tell_partner": "Расскажите партнёру о важности тестирования анонимно 🙋‍♀",
    "project_news": "Новости проекта 📌",
    "social_networks": "Мы в социальных сетях 🔈",
    "get_users": "Получить базу пользователей"
}


class MenuKeyboardBuilder:
    def __init__(self):
        self.__keyboard = ReplyKeyboardMarkup(row_width=1)
        self.__buttons = []

    def __add_menu_buttons(self):
        hiv_risk_assessment_button = KeyboardButton(MENU_BUTTONS_TEXTS["hiv_risk_assessment"])
        info_files_button = KeyboardButton(MENU_BUTTONS_TEXTS["info_files"])
        order_vih_test_button = KeyboardButton(MENU_BUTTONS_TEXTS["order_vih_test"])
        tell_partner_button = KeyboardButton(MENU_BUTTONS_TEXTS["tell_partner"])
        project_news_button = KeyboardButton(MENU_BUTTONS_TEXTS["project_news"])
        social_medias_button = KeyboardButton(MENU_BUTTONS_TEXTS["social_networks"])

        self.__buttons.extend(
            [
                hiv_risk_assessment_button,
                info_files_button,
                order_vih_test_button,
                tell_partner_button,
                project_news_button,
                social_medias_button
            ])
        return True

    def __form_keyboard(self):
        self.__keyboard.add(*self.__buttons)
        return True

    def __add_admin_buttons(self):
        admin_button = KeyboardButton('Получить базу пользователей')
        self.__buttons.extend([admin_button])
        return True

    def get_keyboard(self, user):
        self.__add_menu_buttons()

        if is_admin(user):
            self.__add_admin_buttons()

        self.__form_keyboard()
        return self.__keyboard

