# ВЫСОКИЙ РИСК
high_risk_ru = """
РЕЗУЛЬТАТЫ
Высокий риск: 

22-38 баллов

У Вас довольно высокий риск инфицирования ВИЧ. Рекомендуем Вам как можно раньше начать ДКП 
(это приём препаратов, которые снижают вероятность инфицирования ВИЧ на 98%. При этом 2% приходятся
скорее на погрешности в приёме препаратов, нежели на эффективность такой профилактики. Это значит, что
даже при незащищённом сексе с ВИЧ-позитивным человеком вероятность инфицирования сводится на нет). Вам
подойдет схема с ежедневным приемом препарата. Вы можете избежать инфицирования ВИЧ, если будете
принимать назначенный препарат регулярно, без пропусков и своевременно сдавать необходимые
клинико-лабораторные анализы.\n\nДополнительную информацию
Вы можете узнать у консультанта: @Community_friends_tg
"""

high_risk_kz = """
РЕЗУЛЬТАТЫ
Высокий риск:

22-38 балл

Сізде АҚТҚ жұқтыру қаупі айтарлықтай жоғары. 
PrEP мүмкіндігінше ертерек бастауды ұсынамыз. Сізге препаратты күнделікті қабылдау режимі қолайлы. 
Тағайындалған дәрі-дәрмекті үзіліссіз, жүйелі түрде қабылдап, қажетті клиникалық және зертханалық 
зерттеулерді дер кезінде өткізіп отырсаңыз, АИТВ-ны жұқтырудан аулақ бола аласыз.

Қосымша ақпарат 
алу үшін кеңесшіңізге хабарласыңыз: @Community_friends_tg
"""

# СРЕДНИЙ РИСК
medium_risk_ru = """
РЕЗУЛЬТАТЫ
Средний риск:

7-21 балл

У Вас есть риск инфицирования ВИЧ. Рекомендуем Вам начать ДКП (это приём препаратов, которые 
снижают вероятность инфицирования ВИЧ на 98%. При этом 2% приходятся скорее на погрешности в приёме 
препаратов, нежели на эффективность такой профилактики. Это значит, что даже при незащищёном сексе 
с ВИЧ-позитивным человеком вероятность инфицирования сводится на нет) в ближайшее время. Вы можете 
обсудить с врачом удобную для Вас схему приема препарата, главное соблюдать все медицинские 
рекомендации, и Вы сможете избежать инфицирования ВИЧ.\n\nДополнительную информацию Вы можете узнать 
у консультанта: @Community_friends_tg
"""

medium_risk_kz = """
РЕЗУЛЬТАТЫ
Средний риск:

7-21 балл 

АИТВ жұқтыру қаупі бар. PrEP мүмкіндігінше тезірек 
бастауды ұсынамыз. Сіз дәрігермен препаратты қабылдаудың ыңғайлы режимін талқылай аласыз, ең 
бастысы - барлық медициналық ұсыныстарды орындау, және сіз АИТВ-ны жұқтырудан аулақ бола 
аласыз.

Қосымша ақпарат 
алу үшін кеңесшіңізге хабарласыңыз: @Community_friends_tg
"""

# НИЗКИЙ РИСК
small_risk_ru = """
РЕЗУЛЬТАТЫ
Низкий риск:

Менее 7 баллов 

У вас низкий риск инфицирования ВИЧ.
Дополнительную информацию о способах защиты
от ВИЧ и ИППП Вы можете узнать у консультанта: @Community_friends_tg             
"""

small_risk_kz = """
РЕЗУЛЬТАТЫ
Низкий риск:

7 баллдан аз
 
сізде АҚТҚ жұқтыру қаупі төмен. Өзіңізді АИТВ және
ЖЖБИ-ден қорғау жолдары туралы қосымша ақпарат алу үшін кеңесшіден сұрай аласыз: @Community_friends_tg
"""

risk_ratings_kz = {
    "small": small_risk_kz,
    "high": high_risk_kz,
    "medium": medium_risk_kz
}

risk_ratings_ru = {
    "small": small_risk_ru,
    "high": high_risk_ru,
    "medium": medium_risk_ru
}
# ТЕКСТЫ ВОПРОСОВ НА ДВУХ ЯЗЫКАХ
question_1_ru_text = "Ваш партнер является ВИЧ-положительным человеком?"
question_2_ru_text = "Получает ли партнер препараты для лечения ВИЧ?"
question_3_ru_text = "Получает ли партнер препараты для лечения ВИЧ более 6 месяцев?"
question_4_ru_text = "Регулярно ли вы обсуждаете приверженность партнера лечению ВИЧ (т.е. как минимум, раз в месяц)?"
question_5_ru_text = "Знаете ли Вы последние результаты определения вирусной нагрузки своего партнера?"
question_6_ru_text = "Хотите ли Вы иметь общего ребенка со своим партнером?"
question_7_ru_text = "Постоянно ли Вы и Ваш партнер пользуетесь презервативами?"
question_8_ru_text = "Указывают ли какие-то аспекты Вашей жизни на повышенный риск ВИЧ-инфицирования?"
question_9_ru_text = "Вы получали деньги, жилье, еду или подарки в обмен на секс?"
question_10_ru_text = "Вас принуждали к сексу против Вашей воли?"

question_11_ru_text = """
Вы подвергались физическому насилию или рукоприкладству со стороны другого лица,в том числе со стороны полового партнера?
"""

question_12_ru_text = """
Вы принимали  ПКП (постконтактная профилактика – 4-недельный курс антиретровирусных препаратов 
для ВИЧ-отрицательных людей, который назначается после ситуаций, влекущих заражение ВИЧ. 
Это может быть незащищённый половой контакт, инъекционное употребление наркотиков или контакт с 
биологическими жидкостями инфицированного человека) для предотвращения ВИЧ-инфицирования?
"""

question_13_ru_text = """
У Вас были ИППП (инфекции, передающиеся половым путем: сифилис, гонорея, хламидиоз, трихомониаз, кандиломы)?
"""

question_14_ru_text = """
Вводили ли Вы инъекции препаратов или гормональных средств, используя общее инъекционное 
оборудование с кем-то другим?
"""

question_15_ru_text = "Употребляли ли Вы легкие наркотики или психотропные препараты за последние полгода?"
question_16_ru_text = "За последние полгода:\nБыло ли у Вас несколько половых партнеров?"
question_17_ru_text = "Были ли у Вас половые контакты без презерватива?"
question_18_ru_text = "Были ли у Вас половые контакты с людьми, ВИЧ-статус которых Вы не знаете?"
question_19_ru_text = "Подвержен ли кто-либо из Ваших партнеров риску ВИЧ-инфицирования?"
question_20_ru_text = "Были ли у Вас половые контакты с ВИЧ-инфицированным лицом?"
question_21_ru_text = "Занимались ли вы сексом с использованием психоактивных/наркотических веществ?"

question_1_ru = {
    "question_text": question_1_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}

question_2_ru = {
    "question_text": question_2_ru_text,
    "answers": {
        "Да": 0,
        "Нет": 2,
        "Не знаю": 1
    }
}

question_3_ru = {
    "question_text": question_3_ru_text,
    "answers": {
        "Да": 0,
        "Нет": 2,
        "Не знаю": 1
    }
}

question_4_ru = {
    "question_text": question_4_ru_text,
    "answers": {
        "Да": 0,
        "Нет": 1
    }
}
question_5_ru = {
    "question_text": question_5_ru_text,
    "answers": {
        "Да": 0,
        "Нет": 1
    }
}
question_6_ru = {
    "question_text": question_6_ru_text,
    "answers": {
        "Да": 1,
        "Нет": 0,
        "Не задумывался/лась": 0
    }
}
question_7_ru = {
    "question_text": question_7_ru_text,
    "answers": {
        "Да": 0,
        "Нет": 1,
    }
}
question_8_ru = {
    "question_text": question_8_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0,
        "Не знаю": 1
    }
}
question_9_ru = {
    "question_text": question_9_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_10_ru = {
    "question_text": question_10_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0,
    }
}
question_11_ru = {
    "question_text": question_11_ru_text,
    "answers": {
        "Да": 1,
        "Нет": 0,
        "Не задумывался/лась": 0
    }
}
question_12_ru = {
    "question_text": question_12_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_13_ru = {
    "question_text": question_13_ru_text,
    "answers": {
        "Да": 1,
        "Нет": 0,
        "Не проверялся": 1
    }
}
question_14_ru = {
    "question_text": question_14_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_15_ru = {
    "question_text": question_15_ru_text,
    "answers": {
        "Да": 3,
        "Нет": 0
    }
}
question_16_ru = {
    "question_text": question_16_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_17_ru = {
    "question_text": question_17_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_18_ru = {
    "question_text": question_18_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_19_ru = {
    "question_text": question_19_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0,
        "Не знаю": 1
    }
}
question_20_ru = {
    "question_text": question_20_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
    }
}
question_21_ru = {
    "question_text": question_21_ru_text,
    "answers": {
        "Да": 2,
        "Нет": 0
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
        "question_21": question_21_ru,
    }


question_1_kz_text = "Сіздің серіктесіңіз АҚТҚ жұқты ма?"
question_2_kz_text = "Серіктес АИТВ-мен емдеу үшін АРТ қабылдап жатыр ма?"
question_3_kz_text = "Серіктес 6 айдан астам уақыт бойы АИТВ-ға қарсы дәрі-дәрмек қабылдаған ба?"
question_4_kz_text = "Сіз серіктесіңіздің АҚТҚ-ны емдеуді ұстануын үнемі (яғни, айына бір рет) талқылайсыз ба?"
question_5_kz_text = "Сіз серіктесіңіздің соңғы вирустық жүктеме нәтижелерін білесіз бе?"
question_6_kz_text = "Серіктесіңізден балалы болғыңыз келе ме?"
question_7_kz_text = "Сіз және сіздің серіктесіңіз презервативтерді үнемі пайдаланасыз ба?"
question_8_kz_text = "Сіздің өміріңіздің қандай да бір аспектілері АҚТҚ жұқтыру қаупінің жоғарылауын көрсете ме?"
question_9_kz_text = "Сіз жыныстық қатынас үшін ақша, баспана, тамақ немесе сыйлықтар алдыңыз ба?"
question_10_kz_text = "Сіз өз еркіңізге қарсы жыныстық қатынасқа түсуге мәжбүр болдыңыз ба?"

question_11_kz_text = """
Сізге басқа адам, соның ішінде жыныстық серіктес тарапынан физикалық зорлық-зомбылық немесе ұрып-соғу болды ма?
"""

question_12_kz_text = """
Сіз АИВ-инфекциясы бар жағдайлардан кейін берілген PEP (экспозициядан кейінгі профилактика – 
АИТВ-теріс адамдарға арналған ретровирусқа қарсы препараттардың 4 апталық курсы) қабылдадыңыз. 
Бұл қорғалмаған жыныстық қатынас, инъекциялық есірткі қолдану немесе жұқтырған адамның дене 
сұйықтығымен әсер ету болуы мүмкін. адам) АИТВ инфекциясының алдын алу үшін?
"""

question_13_kz_text = """
Сізде ЖЖБИ (жыныстық жолмен берілетін инфекциялар: мерез, гонорея, хламидиоз, трихомониаз, кондиломалар) болды ма?
"""

question_14_kz_text = "Сіз инъекциялық жабдықты басқа біреумен бөлісу кезінде есірткі немесе гормондарды енгіздіңіз бе?"
question_15_kz_text = "Сіз соңғы алты айда жұмсақ препараттарды немесе психотроптық препараттарды қолдандыңыз ба?"
question_16_kz_text = "Соңғы алты айда:\nСізде бірнеше жыныстық серіктес болды ма?"
question_17_kz_text = "Сіз презервативсіз жыныстық қатынаста болдыңыз ба?"
question_18_kz_text = "Сіз АИТВ статусын білмейтін адамдармен жыныстық қатынаста болдыңыз ба?"
question_19_kz_text = "Сіздің серіктестеріңізде АҚТҚ жұқтыру қаупі бар ма?"
question_20_kz_text = "АИТВ жұқтырған адаммен жыныстық қатынаста болдыңыз ба?"
question_21_kz_text = "Сіз психоактивті/есірткілермен жыныстық қатынаста болдыңыз ба?"


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
question_21_kz = {
    "question_text": question_21_kz_text,
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
        "question_21": question_21_kz,
    }

