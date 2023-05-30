import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

# Объект бота
bot = Bot(token=os.getenv('TOKEN'))
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.DEBUG)


# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.reply("""Здравствуйте! Какой у вас домашний любимец?)\n 
                        Если у вас есть вопросы или предложения - напишите нашему менеджеру!\n 
                        Контакты:""")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
