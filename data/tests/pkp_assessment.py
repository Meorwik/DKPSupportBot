# ВЫСОКИЙ РИСК
high_result_ru = """
8-10:
Высокая срочность для начала ПКП. Рекомендуется немедленная медицинская помощь.
"""

high_result_kz = """
"""

# СРЕДНИЙ РИСК
medium_result_ru = """
4-7:
Умеренная срочность для начала ПКП. Рекомендуется немедленная консультация с врачом.
"""

medium_result_kz = """

"""

# НИЗКИЙ РИСК
small_result_ru = """
0-3:
Низкая срочность для начала ПКП. Проконсультируйтесь с врачом для получения дальнейших указаний.
"""

small_result_kz = """

"""

result_ratings_kz = {
    "small": small_result_kz,
    "high": high_result_kz,
    "medium": medium_result_kz
}

result_ratings_ru = {
    "small": small_result_ru,
    "high": high_result_ru,
    "medium": medium_result_ru
}
# ТЕКСТЫ ВОПРОСОВ НА ДВУХ ЯЗЫКАХ
question_1_ru_text = """
**Какой контакт имел место с потенциальным носителем ВИЧ?**

A) Контакта не было

B) Случайный контакт (рукопожатие, объятия)

C) Половой контакт без проникновения (поцелуи, взаимная мастурбация)

D) Проникающий половой контакт (незащищённый вагинальный или анальный половой акт) 
"""

question_2_ru_text = """

"""

question_3_ru_text = """

"""

question_4_ru_text = """

"""

question_5_ru_text = """

"""

question_6_ru_text = """

"""

question_7_ru_text = """

"""

question_8_ru_text = """

"""

question_9_ru_text = """

"""

question_10_ru_text = """

"""


question_1_ru = {
    "question_text": question_1_ru_text,
    "answers": {
        "Ответ A": 0,
        "Ответ B": 0,
        "Ответ C": 0,
        "Ответ D": 1
    }
}

question_2_ru = {
    "question_text": question_2_ru_text,
    "answers": {
        "Ответ A": 1,
        "Ответ B": 0,
        "Ответ C": 0,
        "Ответ D": 0
    }
}

question_3_ru = {
    "question_text": question_3_ru_text,
    "answers": {
        "Ответ A": 1,
        "Ответ B": 0,
        "Ответ C": 0
    }
}

question_4_ru = {
    "question_text": question_4_ru_text,
    "answers": {
        "Ответ A": 1,
        "Ответ B": 0,
    }
}

question_5_ru = {
    "question_text": question_5_ru_text,
    "answers": {
        "Ответ A": 0,
        "Ответ B": 1,
    }
}

question_6_ru = {
    "question_text": question_6_ru_text,
    "answers": {
        "Ответ A": 0,
        "Ответ B": 1,
    }
}

question_7_ru = {
    "question_text": question_7_ru_text,
    "answers": {
        "Ответ A": 0,
        "Ответ B": 1,
    }
}

question_8_ru = {
    "question_text": question_8_ru_text,
    "answers": {
        "Ответ A": 1,
        "Ответ B": 0,
    }
}

question_9_ru = {
    "question_text": question_9_ru_text,
    "answers": {
        "Ответ A": 1,
        "Ответ B": 0,
    }
}

question_10_ru = {
    "question_text": question_10_ru_text,
    "answers": {
        "Ответ A": 0,
        "Ответ B": 0,
        "Ответ C": 1
    }
}

questions_ru = \
    {
        "question_1": question_1_ru,
        "question_2": question_2_ru,
        "question_3": question_3_ru,
        "question_4": question_4_ru,
        "question_5": question_5_ru,
        "question_6": question_6_ru,
        "question_7": question_7_ru,
        "question_8": question_8_ru,
        "question_9": question_9_ru,
        "question_10": question_10_ru
    }