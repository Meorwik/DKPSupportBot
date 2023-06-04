from aiogram import Dispatcher
from data.config import ADMINS
import logging


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")

        except Exception as err:
            logging.exception(err)
