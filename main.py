import argparse
import asyncio
import sys

from loguru import logger
import config
from config import LOG_LEVEL

logger.remove()
logger.add(
    sink=sys.stdout,
    level=config.LOG_LEVEL,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
)

if __name__ == '__main__':
    logger.add('log/{time:DD_MM_YYYY}.log', level=LOG_LEVEL, rotation='12:00')
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", choices=["tg", "vk", "api"], required=True)
    args = parser.parse_args()

    if args.bot == "tg":
        from tg import bot, dp


        async def main():
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info('TG бот запущен')
            await dp.start_polling(bot)

        asyncio.run(main())

    elif args.bot == "vk":
        from vk.bot import bot

        logger.info('VK бот запущен')
        bot.run()
    elif args.bot == "api":
        import uvicorn

        logger.info(f'API запущен на {config.API_HOST}:{config.API_PORT}')
        uvicorn.run("api.main:app", host=config.API_HOST, port=config.API_PORT, log_level=LOG_LEVEL)
