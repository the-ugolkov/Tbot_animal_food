import os

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv

# Подгружаем переменные окружения
load_dotenv()

# Объявление и инициализация объектов бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

# Объявляем настройки базы данных
# (так же они есть в .env, но вынес сюда для простоты запуска бота с минимальными настройками перед сборкой контейнеров)
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_LOGIN = 'postgres'
DB_PASS = 'postgres'
DB_NAME = 'postgres'

# Объявляем команды для меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/food", description="Выбрать корм")
    ]
    await bot.set_my_commands(commands)
