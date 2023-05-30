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


# Устанавливаем команды для меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/food", description="Выбрать корм")
    ]
    await bot.set_my_commands(commands)
