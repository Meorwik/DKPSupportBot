from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.connection_configs import ConnectionConfig
from utils.db_api.db_api import PostgresDataBaseManager
from aiogram import Bot, Dispatcher, types
from pytz import timezone
from data import config


KZ_TIMEZONE = timezone("Asia/Almaty")
scheduler = AsyncIOScheduler(
    timezone=KZ_TIMEZONE
)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
postgres_manager = PostgresDataBaseManager(ConnectionConfig.get_postgres_connection_config())
