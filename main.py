import argparse
import sys

from loguru import logger
import config


logger.remove()
logger.add(
    sink=sys.stdout,
    level=config.LOG_LEVEL,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
)

if __name__ == '__main__':
    logger.add('log/{time:DD_MM_YYYY}.log', level="INFO", rotation='12:00')
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", choices=["tg", "vk"], required=True)
    args = parser.parse_args()

    if args.bot == "tg":
        logger.critical("TG bot is not supported")
    elif args.bot == "vk":
        from vk import bot as vk_bot
        vk_bot.run()
