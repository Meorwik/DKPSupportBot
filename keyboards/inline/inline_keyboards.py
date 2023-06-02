from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle
from aiogram import types

# КЛАСС: TestKeyboardBuilder
# Создан для создания клавиатур на основе которых будут работать тесты,
# принимает на вход данные теста и возвращает список со всеми клавиатурами
class TestKeyboardBuilder:
    def __init__(self):
        self.questions = None

    def __unpack_test_materials(self, test_materials):
        self.questions = test_materials["questions"]

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

            shuffle(buttons)
            question_text = question["question_text"]
            product = {"text": question_text, "keyboard": InlineKeyboardMarkup(row_width=1).add(*buttons)}
            keyboards[f"question_{question_number}"] = product
        return keyboards

    def get_keyboards(self, test_materials):
        self.__unpack_test_materials(test_materials=test_materials)

        return self.__create_keyboards()

# КЛАССЖ: SimpleKeyboardBuilder
# Создан для работы с простыми клавиатурами и мелкими действиями.
class SimpleKeyboardBuilder:
    @classmethod
    def get_social_networks_keyboard(cls):
        facebook_button = InlineKeyboardButton("Перейти в Facebook",
                                               "https://www.facebook.com/groups/communityfriendskz/")

        instagram_button = InlineKeyboardButton("Перейти в Instagram", "https://instagram.com/community__friends")

        return {
            "text": "Facebook и Instagram страница проекта",
            "keyboard": InlineKeyboardMarkup(row_width=1).add(instagram_button, facebook_button)
        }

    @classmethod
    def get_project_news_keyboards(cls):
        first_button = InlineKeyboardButton("Перейти", "https://www.facebook.com/AMECAlmaty/posts/313432297466945")

        second_button = InlineKeyboardButton\
            (
                text="Перейти",
                url="https://www.the-village-kz.com/village/city/news-city/19155-dokontaktnaya-profilaktika-novyy-sposob-profilaktiki-vich-v-kazahstane"
            )

        first_product = {
            "text": "О ВИЧ рассказывают подростки",
            "keyboard": InlineKeyboardMarkup().add(first_button)
        }

        second_product = {
            "text": "Доконтактная профилактика: Новый способ профилактики ВИЧ в Казахстане",
            "keyboard": InlineKeyboardMarkup().add(second_button)
        }

        return first_product, second_product

    @classmethod
    def get_tell_partner_keyboard(cls):
        tell_partner_button = InlineKeyboardButton("Перейти", "https://sms.icapapps.kz/ru/")
        return {
            "text": "Расскажите партнёру о важности тестирования анонимно 🙋‍♀",
            "keyboard": InlineKeyboardMarkup().add(tell_partner_button)
        }

    @classmethod
    def get_language_selection_documents_keyboard(cls):
        send_kz_document = InlineKeyboardButton(text="Қазақша", callback_data="send_document_KZ")
        send_ru_document = InlineKeyboardButton(text="Русский", callback_data="send_document_RU")
        ask_language = "Выберите язык, чтобы продолжить:"

        return {
            "text": ask_language,
            "keyboard": InlineKeyboardMarkup(row_width=1).add(send_ru_document, send_kz_document)
        }

    @classmethod
    def get_back_to_menu_keyboard(cls):
        back_to_menu = InlineKeyboardButton(text="Назад в меню", callback_data="menu")
        return InlineKeyboardMarkup(row_width=1).add(back_to_menu)

    @classmethod
    def get_language_selection_keyboard(cls, callback):
        ru_button = InlineKeyboardButton(text="Русский", callback_data=f"ru_{callback}")
        kz_button = InlineKeyboardButton(text="Қазақша", callback_data=f"kz_{callback}")
        language_select_keyboard = InlineKeyboardMarkup(row_width=1).add(ru_button, kz_button)
        return language_select_keyboard