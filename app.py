from utils.set_bot_commands import set_default_commands
from loader import dp, postgres_manager, scheduler
from aiogram import executor
import handlers


async def on_startup(dispatcher):
    scheduler.start()

    await postgres_manager.create_users_table()
    await postgres_manager.create_tests_table()
    await postgres_manager.create_logs_table()
    await postgres_manager.create_medication_schedule_table()

    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

