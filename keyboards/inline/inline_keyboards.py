from data.assessments.assessments_manager import WRONG_POSSIBLE_ASSESSMENT_TYPE
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

MEDICAL_SCHEDULE_BUTTON_MATERIALS = {
    "note_taking_medications": "Отметить прием препаратов"
}


# КЛАСС: TestKeyboardBuilder
# Создан для создания клавиатур на основе которых будут работать тесты,
# принимает на вход данные теста и возвращает список со всеми клавиатурами
class AssessmentKeyboardBuilder:
    def __init__(self):
        self.questions = None

    def __unpack_test_materials(self, test_materials):
        self.questions = test_materials["questions"]
        self.assessment_type = test_materials["type"]

    def __create_keyboards(self):
        keyboards = {}
        for question_number in range(1, len(self.questions) + 1):
            question = self.questions[f"question_{question_number}"]
            buttons = \
                [
                    InlineKeyboardButton(text=key, callback_data=str(value))
                    for key, value in
                    question["answers"].items()
                ]

            if self.assessment_type == WRONG_POSSIBLE_ASSESSMENT_TYPE:
                question_text = question["question_text"]
                question_wrong_answer_text = question["wrong_answer_case"]
                product = {
                    "text": question_text,
                    "keyboard": InlineKeyboardMarkup(row_width=1).add(*buttons),
                    "wrong_answer": question_wrong_answer_text
                }

            else:
                question_text = question["question_text"]
                product = {
                    "text": question_text,
                    "keyboard": InlineKeyboardMarkup(row_width=1).add(*buttons),
                }

            keyboards[f"question_{question_number}"] = product

        return keyboards

    def get_keyboards(self, test_materials):
        self.__unpack_test_materials(test_materials=test_materials)

        return self.__create_keyboards()


# КЛАСС: SimpleKeyboardBuilder
# Создан для работы с простыми клавиатурами и мелкими действиями.
class SimpleKeyboardBuilder:
    @classmethod
    def get_social_networks_keyboard(cls):
        facebook_button = InlineKeyboardButton(
            "Перейти в Facebook",
            "https://www.facebook.com/groups/communityfriendskz/"
        )

        instagram_button = InlineKeyboardButton(
            "Перейти в Instagram",
            "https://instagram.com/community__friends"
        )

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(instagram_button, facebook_button)

        return keyboard

    @classmethod
    def get_project_news_keyboards(cls):
        first_button = InlineKeyboardButton("Перейти", "https://www.facebook.com/AMECAlmaty/posts/313432297466945")
        second_button = InlineKeyboardButton(
            text="Перейти",
            url="https://www.the-village-kz.com/village/city/news-city/"
                "19155-dokontaktnaya-profilaktika-novyy-sposob-profilak"
                "tiki-vich-v-kazahstane"
        )

        first_keyboard = InlineKeyboardMarkup().add(first_button)
        second_keyboard = InlineKeyboardMarkup().add(second_button)

        return first_keyboard, second_keyboard

    @classmethod
    def get_tell_partner_keyboard(cls):
        tell_partner_button = InlineKeyboardButton("Перейти", "https://sms.icapapps.kz/ru/")

        keyboard = InlineKeyboardMarkup()
        keyboard.add(tell_partner_button)

        return keyboard

    @classmethod
    def get_language_selection_documents_keyboard(cls):
        send_kz_document = InlineKeyboardButton(text="Қазақша", callback_data="send_document_KZ")
        send_ru_document = InlineKeyboardButton(text="Русский", callback_data="send_document_RU")

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(send_ru_document, send_kz_document)

        return keyboard

    @classmethod
    def get_back_to_menu_keyboard(cls):
        back_to_menu = InlineKeyboardButton(text="Назад в меню", callback_data="menu")
        return InlineKeyboardMarkup(row_width=1).add(back_to_menu)

    @classmethod
    def get_language_selection_keyboard(cls, callback):
        ru_button = InlineKeyboardButton(text="Русский", callback_data=f"ru_{callback}")
        kz_button = InlineKeyboardButton(text="Қазақша", callback_data=f"kz_{callback}")
        language_select_keyboard = InlineKeyboardMarkup(row_width=1).add(ru_button)
        return language_select_keyboard

    @classmethod
    def get_error_keyboard(cls):
        error_button = InlineKeyboardButton("ОШИБКА!", callback_data="error")
        error_keyboard = InlineKeyboardMarkup(row_width=1).add(error_button)
        return error_keyboard

    @classmethod
    def get_rate_consultant_keyboard(cls):
        star_emoji = "⭐️"

        first_star_button = InlineKeyboardButton(star_emoji, callback_data="star_1")
        second_star_button = InlineKeyboardButton(star_emoji, callback_data="star_2")
        third_star_button = InlineKeyboardButton(star_emoji, callback_data="star_3")
        fourth_star_button = InlineKeyboardButton(star_emoji, callback_data="star_4")
        fifth_star_button = InlineKeyboardButton(star_emoji, callback_data="star_5")

        rate_keyboard = InlineKeyboardMarkup(row_width=5)

        rate_keyboard.add(
            first_star_button,
            second_star_button,
            third_star_button,
            fourth_star_button,
            fifth_star_button
        )

        return rate_keyboard

    @classmethod
    def get_note_taking_medications_keyboard(cls):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(
            text=MEDICAL_SCHEDULE_BUTTON_MATERIALS["note_taking_medications"],
            callback_data="note_taking_medications"
        ))
        return keyboard


class PeriodSelector:
    def __init__(self):
        self.__MIN_YEAR = 2023
        self.__MAX_YEAR = 2025
        self.__MONTHS = {
            "Январь": '01',
            "Февраль": '02',
            "Март": '03',
            "Апрель": '04',
            "Май": '05',
            "Июнь": '06',
            "Июль": '07',
            "Август": '08',
            "Сентябрь": '09',
            "Октябрь": '10',
            "Ноябрь": '11',
            "Декабрь": '12'
        }

        self.__keyboard = InlineKeyboardMarkup(row_width=3)

        self.__callback_prefixes = {
            "[monthCallbacks]": "[monthCallbacks]",
            "previous_year": "[backCallback]",
            "next_year": "[forwardCallback]"
        }

        self.__month_buttons = None

    @staticmethod
    def __get_current_year(year):
        if year is None:
            return str(datetime.date.today().year)
        else:
            return year

    def __add_season_buttons(self, first_month, second_month, third_month):
        self.__keyboard.row(
            self.__month_buttons[first_month],
            self.__month_buttons[second_month],
            self.__month_buttons[third_month]
        )

    def __create_months_buttons(self, year=None):
        year = self.__get_current_year(year)

        self.__month_buttons = {
            month_callback: InlineKeyboardButton(
                text=month_name,
                callback_data=f"[monthCallbacks]:{year}-{month_callback}"
            )
            for month_name, month_callback
            in
            self.__MONTHS.items()
        }

        # WINTER
        self.__add_season_buttons("12", "01", "02")
        # SPRING
        self.__add_season_buttons("03", "04", "05")
        # SUMMER
        self.__add_season_buttons("06", "07", "08")
        # AUTUMN
        self.__add_season_buttons("09", "10", "11")

        return True

    def __create_bottom_buttons(self, year=None):
        go_back_button_text = "<<"
        year = self.__get_current_year(year)
        go_forward_button_text = ">>"

        go_back_button_callback = f"[backCallback]:{year}:{go_back_button_text}"
        current_year_button_callback = "None"
        go_forward_button_callback = f"[forwardCallback]:{year}:{go_forward_button_text}"

        go_back_button = InlineKeyboardButton(go_back_button_text, callback_data=go_back_button_callback)
        current_year_button = InlineKeyboardButton(year, callback_data=current_year_button_callback)
        go_forward_button = InlineKeyboardButton(go_forward_button_text, callback_data=go_forward_button_callback)

        self.__keyboard.row(
            go_back_button,
            current_year_button,
            go_forward_button
        )

        return True

    @staticmethod
    def get_callback_components(call):
        callback_separator = ":"
        callback_components = call.data.split(callback_separator)

        if "[backCallback]" in callback_components:
            callback_components = {
                "callback_type": "[backCallback]",
                "year": callback_components[1],
                "button_text": callback_components[2]
            }

        elif "[forwardCallback]" in callback_components:
            callback_components = {
                "callback_type": "[forwardCallback]",
                "year": callback_components[1],
                "button_text": callback_components[2]
            }

        elif "[monthCallbacks]" in callback_components:
            callback_components = {
                "callback_type": "[monthCallbacks]",
                "date": callback_components[1]
            }

        else:
            callback_components = {
                "None": None
            }

        return callback_components

    @classmethod
    def filter_callbacks(cls, call):
        filter_storage = []
        for i in cls().__callback_prefixes.values():
            filter_storage.append(i in call.data)

        return True in filter_storage

    def get_next_year_keyboard(self, call):
        callback_components = self.get_callback_components(call)
        callback_year = int(callback_components["year"])

        if self.__MAX_YEAR == callback_year:
            return self.get_keyboard(self.__MAX_YEAR)

        else:
            return self.get_keyboard(str(callback_year + 1))

    def get_previous_year_keyboard(self, call):
        callback_components = self.get_callback_components(call)
        callback_year = int(callback_components["year"])

        if self.__MIN_YEAR == callback_year:
            return self.get_keyboard(self.__MIN_YEAR)

        else:
            return self.get_keyboard(str(callback_year - 1))

    def get_keyboard(self, year=None):
        self.__create_months_buttons(year)
        self.__create_bottom_buttons(year)

        return self.__keyboard
