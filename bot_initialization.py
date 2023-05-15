from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import logging
from db_api import PostgresDataBaseManager, db_connection_config, DataConvertor, DB_USERS_COLUMNS
import io

TOKEN = '6073444439:AAHkcPtKwycfplfU0VvB48UbNgr8Kw6Knn0'

storage = MemoryStorage()

ADMINS = [912239061, 169707453, 598554856, 793520950]
db = PostgresDataBaseManager(db_connection_config)
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('bot: Бот вышел в онлайн!')
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Команда start для запуска бота")
        ]
    )


class test_language(StatesGroup):
    language = State()
    temp = State


class the_big_test(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()
    q14 = State()
    q15 = State()
    q16 = State()
    q17 = State()
    q18 = State()
    q19 = State()
    q20 = State()


@dp.message_handler(commands='start', state="*")
async def start(message: types.Message):
    print(message.from_user.username)

    if not message.from_user.username:
        await message.answer('Ваш профиль не имеет логина. Указать его можно в настройках.\n\n'
                             'Инструкция: https://inetfishki.ru/telegram/kak-uznat-dobavit-pomenyat-login.html#i-4')
    else:
        db.check_user(message.from_user)
        start_btn = InlineKeyboardButton('Начать!', callback_data='menu')
        start_kb = InlineKeyboardMarkup(row_width=2).add(start_btn)
        await message.answer('Здравствуйте!\n'
                             'Я – бот, который поможет Вам оценить риск инфицирования ВИЧ и понять, '
                             'нужны ли услуги по профилактике ВИЧ. \nНажмите "Начать!", чтобы продолжить:',
                             reply_markup=start_kb)


# ОСНОВНОЕ МЕНЮ
@dp.callback_query_handler(lambda c: c.data == 'menu')
async def menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    test_btn = KeyboardButton('Тест на оценку риска инфицирования ВИЧ 📋')
    files_btn = KeyboardButton('Всё о доконтактной профилактике ВИЧ 📚')
    admin_btn = KeyboardButton('Получить базу пользователей')
    free_test_btn = KeyboardButton('Заказать бесплатный тест на ВИЧ 💊')
    ask_btn = KeyboardButton('Расскажите партнёру о важности тестирования анонимно 🙋‍♀')
    project_news_btn = KeyboardButton('Новости проекта 📌')
    social_medias_btn = KeyboardButton('Мы в социальных сетях 🔈')
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(test_btn).add(files_btn).add(free_test_btn) \
        .add(ask_btn).add(project_news_btn, social_medias_btn)
    if callback_query.from_user.id in ADMINS:
        menu_kb.add(admin_btn)
    await bot.send_message(callback_query.from_user.id, 'Меню', reply_markup=menu_kb)


@dp.message_handler(lambda message: message.from_user.id in ADMINS, text="Получить базу пользователей")
async def test(callback_query: types.CallbackQuery):
    file_name = "users"
    users_data = db.get_all_users()
    data_convertor = DataConvertor()
    saved_file_path = await data_convertor.convert_to_exel(users_data, DB_USERS_COLUMNS, file_name)

    with open(saved_file_path, "rb") as exel_users_data:
        await bot.send_document(chat_id=callback_query.from_user.id, document=exel_users_data)


@dp.message_handler(text="Всё о доконтактной профилактике ВИЧ 📚")
async def test(callback_query: types.CallbackQuery):
    ask_language = "Выберите язык, чтобы продолжить:"
    kz_button = InlineKeyboardButton("Қазақша", callback_data="KZ")
    ru_button = InlineKeyboardButton("Русский", callback_data="RU")

    kb = InlineKeyboardMarkup().add(kz_button, ru_button)

    await bot.send_message(text=ask_language, reply_markup=kb, chat_id=callback_query.from_user.id)


@dp.callback_query_handler(lambda call: call.data == "RU" or call.data == "KZ")
async def send_document(callback_query: types.CallbackQuery):
    if callback_query.data == "RU":
        await callback_query.message.edit_text("Пару секунд, загружаю информацию...")

        with io.open("Что такое ДКП ВИЧ.pdf", "rb") as ru_document:
            await bot.send_document(callback_query.from_user.id, document=ru_document)

    elif callback_query.data == "KZ":
        await callback_query.message.edit_text("Бірнеше секунд, ақпаратты жүктеп салу...")

        with io.open("КДП дегеніміз не.pdf", "rb") as kz_document:
            await bot.send_document(callback_query.from_user.id, document=kz_document)

    await callback_query.message.delete()

@dp.message_handler(text="Заказать бесплатный тест на ВИЧ 💊")
async def files(message: types.Message):
    btn = InlineKeyboardButton("Перейти", url="https://hivtest.kz/")
    await message.answer('Заказать бесплатный тест', reply_markup=InlineKeyboardMarkup().add(btn))


@dp.message_handler(text="Расскажите партнёру о важности тестирования анонимно 🙋‍♀")
async def files(message: types.Message):
    btn = InlineKeyboardButton("Перейти", url="https://sms.icapapps.kz/ru/")
    await message.answer('Расскажите партнёру о важности тестирования анонимно 🙋‍♀', reply_markup=InlineKeyboardMarkup().add(btn))


@dp.message_handler(text="Новости проекта 📌")
async def files(message: types.Message):
    btn1 = InlineKeyboardButton("Перейти", url="https://www.facebook.com/AMECAlmaty/posts/313432297466945")
    btn2 = InlineKeyboardButton("Перейти", url="https://www.the-village-kz.com/village/city/news-city/19155-dokontaktnaya-profilaktika-novyy-sposob-profilaktiki-vich-v-kazahstane")
    await message.answer('О ВИЧ рассказывают подростки', reply_markup=InlineKeyboardMarkup().add(btn1))
    await message.answer('Доконтактная профилактика: Новый способ профилактики ВИЧ в Казахстане', reply_markup=InlineKeyboardMarkup().add(btn2))


@dp.message_handler(text="Мы в социальных сетях 🔈")
async def files(message: types.Message):
    btn1 = InlineKeyboardButton("Перейти в Facebook", url="https://www.facebook.com/groups/communityfriendskz/")
    btn2 = InlineKeyboardButton("Перейти в Instagram", url="https://instagram.com/community__friends")
    await message.answer('Facebook и Instagram страница проекта', reply_markup=InlineKeyboardMarkup().add(btn1, btn2))


@dp.message_handler(content_types=["document"])
async def files(message: types.Message):
    await message.answer(message.document.file_id)


# ТЕСТИРОВАНИЕ НА ОЦЕНКУ РИСКА
@dp.message_handler(text="Тест на оценку риска инфицирования ВИЧ 📋")
async def test(callback_query: types.CallbackQuery):
    markup = types.ReplyKeyboardRemove()
    await bot.send_message(callback_query.from_user.id, "Меню скрыто!", reply_markup=markup)
    rus_btn = InlineKeyboardButton('Русский', callback_data='ru')
    kz_btn = InlineKeyboardButton('Қазақша', callback_data='kz')
    language = InlineKeyboardMarkup(row_width=2).add(rus_btn).add(kz_btn)
    await bot.send_message(callback_query.from_user.id, 'Выберите язык, чтобы продолжить:',
                           reply_markup=language)
    await test_language.language.set()


@dp.callback_query_handler(state=test_language.language)
async def start_test(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["lan"] = callback_query.data
    start_test_btn = InlineKeyboardButton('Начать!', callback_data='start_test')
    start_test_kb = InlineKeyboardMarkup(row_width=2).add(start_test_btn)
    if callback_query.data == 'ru':
        await bot.send_message(callback_query.from_user.id, 'Отлично! Выбран русский язык.\nНажмите "Начать!" '
                                                            'для начала теста.', reply_markup=start_test_kb)
    else:
        await bot.send_message(callback_query.from_user.id,
                               'Отлично! Выбран казахский язык.\nНажмите "Начать!" для начала теста.',
                               reply_markup=start_test_kb)
    await test_language.next()


@dp.callback_query_handler(lambda c: c.data == 'start_test')
async def q1(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        language = data['lan']
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    print(language)
    if language == "ru":
        yes_btn = InlineKeyboardButton('Да', callback_data='big_test')
        no_btn = InlineKeyboardButton('Нет', callback_data='small_test')
        yes_no_kb = InlineKeyboardMarkup(row_width=2).add(yes_btn).add(no_btn)
        await bot.send_message(callback_query.from_user.id, texts.question_1_ru, reply_markup=yes_no_kb)
    else:
        yes_btn = InlineKeyboardButton('Иә', callback_data='big_test')
        no_btn = InlineKeyboardButton('Жоқ', callback_data='small_test')
        yes_no_kb = InlineKeyboardMarkup(row_width=2).add(yes_btn).add(no_btn)
        await bot.send_message(callback_query.from_user.id, texts.question_1_kz, reply_markup=yes_no_kb)


@dp.callback_query_handler(lambda c: c.data == 'big_test')
async def q2(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_2_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_2_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_2_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_2_kz, reply_markup=yes_no_kb)
    await the_big_test.q1.set()


@dp.callback_query_handler(lambda c: c.data == 'small_test')
async def small_test(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        language = data['lan']
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_8_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_8_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_8_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_8_kz, reply_markup=yes_no_kb)
    await the_big_test.q7.set()


@dp.callback_query_handler(state=the_big_test.q1)
async def q3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q1"] = int(callback_query.data) + 3
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_3_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_3_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_3_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_3_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q2)
async def q4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q2"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_4_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_4_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_4_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_4_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q3)
async def q5(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q3"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_5_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_5_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_5_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_5_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q4)
async def q6(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q4"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_6_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_6_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_6_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_6_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q5)
async def q7(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q5"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_7_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_7_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_7_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_7_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q6)
async def q8(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q6"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_8_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_8_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_8_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_8_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q7)
async def q9(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q7"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_9_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_9_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_9_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_9_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q8)
async def q10(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q8"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_10_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_10_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_10_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_10_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q9)
async def q11(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q9"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_11_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_11_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_11_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_11_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q10)
async def q12(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q10"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_12_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_12_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_12_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_12_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q11)
async def q13(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q11"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_13_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_13_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_13_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_13_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q12)
async def q14(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q12"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_14_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_14_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_14_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_14_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q13)
async def q15(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q13"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_15_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_15_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_15_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_15_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q14)
async def q16(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q14"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_16_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_16_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_16_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_16_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q15)
async def q17(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q15"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_17_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_17_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_17_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_17_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q16)
async def q18(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q16"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_18_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_18_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_18_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_18_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q17)
async def q19(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q17"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_19_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_19_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_19_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_19_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q18)
async def q20(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q18"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_20_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_20_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_20_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_20_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q19)
async def q21(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        data["q19"] = int(callback_query.data)
    async with state.proxy() as data:
        language = data['lan']
    if language == "ru":
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_21_ru:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_21_ru, reply_markup=yes_no_kb)
    else:
        yes_no_kb = InlineKeyboardMarkup(row_width=2)
        for button in texts.buttons_21_kz:
            btn = InlineKeyboardButton(button[0], callback_data=button[1])
            yes_no_kb.add(btn)
        await bot.send_message(callback_query.from_user.id, texts.question_21_kz, reply_markup=yes_no_kb)
    await the_big_test.next()


@dp.callback_query_handler(state=the_big_test.q20)
async def q_res(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    async with state.proxy() as data:
        language = data['lan']
        data.pop('lan')
    async with state.proxy() as data:
        data["q20"] = int(callback_query.data)
        print(data)
        print(data.values())
    total = sum(data.values())
    menu_btn = InlineKeyboardButton('Назад в меню', callback_data='menu')
    menu_kb = InlineKeyboardMarkup(row_width=2).add(menu_btn)
    if language == "ru":
        if total < 7:
            await bot.send_message(callback_query.from_user.id, texts.small_risk_ru, reply_markup=menu_kb)
        elif total < 21:
            await bot.send_message(callback_query.from_user.id, texts.medium_risk_ru, reply_markup=menu_kb)
        else:
            await bot.send_message(callback_query.from_user.id, texts.high_risk_ru, reply_markup=menu_kb)
    else:
        if total < 7:
            await bot.send_message(callback_query.from_user.id, texts.small_risk_kz, reply_markup=menu_kb)
        elif total < 21:
            await bot.send_message(callback_query.from_user.id, texts.medium_risk_kz, reply_markup=menu_kb)
        else:
            await bot.send_message(callback_query.from_user.id, texts.high_risk_kz, reply_markup=menu_kb)
    await the_big_test.next()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
