import asyncio
import logging

from handlers import register_handlers

from setting import bot, dp, set_commands

logger = logging.getLogger(__name__)


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Регистрация хэндлеров
    register_handlers(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
