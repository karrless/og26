import argparse
import sys

from loguru import logger
import os
import config

logger.remove()
logger.add(
    sink=sys.stdout,
    level=config.LOG_LEVEL,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
)

if __name__ == '__main__':
    # Тут импорты разные
    logger.add('log/{time:DD_MM_YYYY}.log', level="INFO", rotation='12:00')
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", choices=["tg", "vk"], required=True)
    args = parser.parse_args()

    logger.info(config.DB_URI)
    if args.bot == "tg":
        logger.info("tg")
    elif args.bot == "vk":
        logger.info("vk")