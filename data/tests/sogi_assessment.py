# ВЫСОКИЙ РИСК
high_result_ru = """
17-20 баллов:
Отлично! У вас есть всестороннее понимание о сексуальной ориентации и гендерной идентичности.
"""

high_result_kz = """

"""

# СРЕДНИЙ РИСК
medium_result_ru = """
10-16 баллов:
Хорошая работа! У вас есть солидная база знаний о сексуальной ориентации и гендерной идентичности.
"""

medium_result_kz = """

"""

# НИЗКИЙ РИСК
small_result_ru = """
0-9 баллов:
Продолжайте учиться! Есть возможности для улучшения вашего понимания о сексуальной ориентации и гендерной идентичности.
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
question_1_ru_text = "Биологический пол означает:"
question_2_ru_text = "Что такое гендер?"
question_3_ru_text = "Что означает трансгендерный переход?"
question_4_ru_text = "Сексуальная ориентация означает:"
question_5_ru_text = "Что такое интерсекс люди?"
question_6_ru_text = "Гендер – в первую очередь:"
question_7_ru_text = "Небинарный означает:"
question_8_ru_text = "Что такое гетеронормативность?"
question_9_ru_text = "Может ли со временем измениться чья-то сексуальная ориентация?"
question_10_ru_text = "Как правильно назвать того, кого привлекают люди того же пола"
question_11_ru_text = "Какой термин описывает кого-то, чья гендерная идентичность совпадает с назначенным полом при рождении?"
question_12_ru_text = "Что означает ЛГБТК+?"
question_13_ru_text = "Каково назначение местоимений?"
question_14_ru_text = "Что значит сделать коминг-аут как ЛГБТК+?"

question_15_ru_text = """
Какую пользу обществу приносит понимание и принятие разнообразной сексуальной ориентации и гендерной идентичности?
"""
question_16_ru_text = "Что значит быть союзником сообщества ЛГБТК+?"
question_17_ru_text = "Что означает термин «цисгендер»?"
question_18_ru_text = "Какова цель празднования гордости ЛГБТК+?"
question_19_ru_text = "Что такое гендерная дисфория?"
question_20_ru_text = "Как общество способствует формированию гендерных ролей и стереотипов?"


question_1_ru = {
    "question_text": question_1_ru_text,
    "answers": {
        "Присвоенный пол при рождении на основе физических характеристик": 1,
        "Сексуальная ориентация": 0,
        "Гендерная идентичность": 0
    }
}

question_2_ru = {
    "question_text": question_2_ru_text,
    "answers": {
        "То же, что биологический пол": 0,
        "Социальная и культурная концепция, охватывающая роли, поведение и ожидания": 1,
        "Сексуальное влечение человека к другим": 0
    }
}

question_3_ru = {
    "question_text": question_3_ru_text,
    "answers": {
        "Процесс смены биологического пола": 0,
        "Процесс согласования своей гендерной идентичности с назначенным полом при рождении": 1,
        "Процесс перехода от одной сексуальной ориентации к другой": 0

    }
}

question_4_ru = {
    "question_text": question_4_ru_text,
    "answers": {
        "То же, что гендерная идентичность": 0,
        "Эмоциональное, романтическое или сексуальное влечение человека к другим": 1,
        "Процесс перехода от одного пола к другому": 0
    }
}

question_5_ru = {
    "question_text": question_5_ru_text,
    "answers": {
        "Люди, не имеющие биологического пола": 0,
        "Люди, чья гендерная идентичность не соответствует общественным ожиданиям": 0,
        "Люди, рожденные с физическими половыми признаками, которые не соответствуют типичным определениям мужчин или женщин": 1

    }
}

question_6_ru = {
    "question_text": question_6_ru_text,
    "answers": {
        "Определяется биологией и генетикой": 0,
        "Социальный конструкт, находящийся под влиянием культурных и социальных норм": 1,
        "То же, что и сексуальная ориентация": 0
    }
}

question_7_ru = {
    "question_text": question_7_ru_text,
    "answers": {
        "Люди, которые идентифицируют себя как мужчинами, так и женщинами": 0,
        "Люди, которые не идентифицируют себя исключительно как мужчины или женщины": 1,
        "Люди, которых привлекают как мужчины, так и женщины": 0
    }
}

question_8_ru = {
    "question_text": question_8_ru_text,
    "answers": {
        "Вера в то, что гетеросексуальность является единственно допустимой сексуальной ориентацией": 1,
        "Вера в то, что гендер является социальной конструкцией": 0,
        "Вера в то, что все люди имеют один и тот же биологический пол": 0
    }
}

question_9_ru = {
    "question_text": question_9_ru_text,
    "answers": {
        "Нет, сексуальная ориентация фиксирована и неизменна": 0,
        "Да, сексуальная ориентация может развиваться или меняться на протяжении всей жизни человека": 1,
        "Сексуальная ориентация не имеет отношения к личности": 0
    }
}

question_10_ru = {
    "question_text": question_10_ru_text,
    "answers": {
        "Гомосексуал": 1,
        "Гетеросексуал": 0,
        "Бисексуал": 0
    }
}

question_11_ru = {
    "question_text": question_11_ru_text,
    "answers": {
        "Трансгендер": 0,
        "Цисгендер": 1,
        "Небинарный": 0
    }
}

question_12_ru = {
    "question_text": question_12_ru_text,
    "answers": {
        "Лесбиянки, геи, бисексуалы, трансгендеры, квир": 1,
        "Долголетие, Рост, Храбрость, Доверие, Качество": 0,
        "Любовь, Щедрость, Красота, Спокойствие, Причудливость": 0
    }
}

question_13_ru = {
    "question_text": question_13_ru_text,
    "answers": {
        "Они указывают на биологический пол человека": 0,
        "Они помогают людям относиться к другим уважительно и точно": 1,
        "Они раскрывают сексуальную ориентацию человека": 0
    }
}

question_14_ru = {
    "question_text": question_14_ru_text,
    "answers": {
        "Публично раскрывать свою сексуальную ориентацию или гендерную идентичность": 1,
        "Пройти медицинские процедуры по смене пола": 0,
        "Отвергать социальные нормы и ожидания": 0
    }
}

question_15_ru = {
    "question_text": question_15_ru_text,
    "answers": {
        "Оно способствует равенству, инклюзивности и уважению всех людей": 1,
        "Не влияет на общество": 0,
        "Это приводит к путанице и хаосу": 0
    }
}

question_16_ru = {
    "question_text": question_16_ru_text,
    "answers": {
        "Идентифицировать себя как ЛГБТК+": 0,
        "Поддерживать и отстаивать права и благополучие представителей ЛГБТК+": 1,
        "Противодействовать правам ЛГБТК+": 0
    }
}

question_17_ru = {
    "question_text": question_17_ru_text,
    "answers": {
        "Имеющие сексуальную ориентацию, отличную от гетеросексуальной": 0,
        "Идентификация с полом, присвоенным при рождении": 1,
        "Отвержение социальных норм пола": 0
    }
}

question_18_ru = {
    "question_text": question_18_ru_text,
    "answers": {
        "Выставлять напоказ свою сексуальную ориентацию или гендерную идентичность": 0,
        "Повышать осведомленность о проблемах ЛГБТК+ и содействовать их принятию": 1,
        "Исключить людей, не являющихся ЛГБТК+": 0
    }
}

question_19_ru = {
    "question_text": question_19_ru_text,
    "answers": {
        "Заболевание, связанное с сексуальной ориентацией": 0,
        "Стресс или дискомфорт, возникающие, когда гендерная идентичность человека не соответствует назначенному ему при рождении полу": 1,
        "Процесс перехода от одного пола к другому": 0
    }
}

question_20_ru = {
    "question_text": question_20_ru_text,
    "answers": {
        "Общество не влияет на гендерные роли и стереотипы": 0,
        "Общество усиливает и увековечивает гендерные роли и стереотипы посредством социализации и средств массовой информации": 1,
        "Гендерные роли и стереотипы основаны исключительно на биологических факторах": 0
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
        "question_10": question_10_ru,
        "question_11": question_11_ru,
        "question_12": question_12_ru,
        "question_13": question_13_ru,
        "question_14": question_14_ru,
        "question_15": question_15_ru,
        "question_16": question_16_ru,
        "question_17": question_17_ru,
        "question_18": question_18_ru,
        "question_19": question_19_ru,
        "question_20": question_20_ru,
    }

question_1_kz_text = ""
question_2_kz_text = ""
question_3_kz_text = ""
question_4_kz_text = ""
question_5_kz_text = ""
question_6_kz_text = ""
question_7_kz_text = ""
question_8_kz_text = ""
question_9_kz_text = ""
question_10_kz_text = ""
question_11_kz_text = ""
question_12_kz_text = ""
question_13_kz_text = ""
question_14_kz_text = ""
question_15_kz_text = ""
question_16_kz_text = ""
question_17_kz_text = ""
question_18_kz_text = ""
question_19_kz_text = ""
question_20_kz_text = ""

question_1_kz = {
    "question_text": question_1_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0,
    }
}

question_2_kz = {
    "question_text": question_2_kz_text,
    "answers": {
        "Иә": 0,
        "Жоқ": 2,
        "Білмеймін": 1
    }
}
question_3_kz = {
    "question_text": question_3_kz_text,
    "answers": {
        "Иә": 0,
        "Жоқ": 2,
        "Білмеймін": 1
    }
}

question_4_kz = {
    "question_text": question_4_kz_text,
    "answers": {
        "Иә": 0,
        "Жоқ": 1
    }
}
question_5_kz = {
    "question_text": question_5_kz_text,
    "answers": {
        "Иә": 0,
        "Жоқ": 1
    }
}
question_6_kz = {
    "question_text": question_6_kz_text,
    "answers": {
        "Иә": 1,
        "Жоқ": 0,
        "Ойланбадым / тырыстым": 0
    }
}
question_7_kz = {
    "question_text": question_7_kz_text,
    "answers": {
        "Иә": 0,
        "Жоқ": 1,
    }
}
question_8_kz = {
    "question_text": question_8_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0,
        "Білмеймін": 1
    }
}
question_9_kz = {
    "question_text": question_9_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_10_kz = {
    "question_text": question_10_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0,
    }
}
question_11_kz = {
    "question_text": question_11_kz_text,
    "answers": {
        "Иә": 1,
        "Жоқ": 0,
        "Не задумывался/лась": 0
    }
}
question_12_kz = {
    "question_text": question_12_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_13_kz = {
    "question_text": question_13_kz_text,
    "answers": {
        "Иә": 1,
        "Жоқ": 0,
        "Тексерілмеген": 1
    }
}
question_14_kz = {
    "question_text": question_14_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_15_kz = {
    "question_text": question_15_kz_text,
    "answers": {
        "Иә": 3,
        "Жоқ": 0
    }
}
question_16_kz = {
    "question_text": question_16_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_17_kz = {
    "question_text": question_17_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_18_kz = {
    "question_text": question_18_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}
question_19_kz = {
    "question_text": question_19_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0,
        "Білмеймін": 1
    }
}
question_20_kz = {
    "question_text": question_20_kz_text,
    "answers": {
        "Иә": 2,
        "Жоқ": 0
    }
}


questions_kz = \
    {
        "question_1": question_1_kz,
        "question_2": question_2_kz,
        "question_3": question_3_kz,
        "question_4": question_4_kz,
        "question_5": question_5_kz,
        "question_6": question_6_kz,
        "question_7": question_7_kz,
        "question_8": question_8_kz,
        "question_9": question_9_kz,
        "question_10": question_10_kz,
        "question_11": question_11_kz,
        "question_12": question_12_kz,
        "question_13": question_13_kz,
        "question_14": question_14_kz,
        "question_15": question_15_kz,
        "question_16": question_16_kz,
        "question_17": question_17_kz,
        "question_18": question_18_kz,
        "question_19": question_19_kz,
        "question_20": question_20_kz,
    }

