from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN, TG_SOCKS

session = AiohttpSession(
    proxy=TG_SOCKS
)

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    storage=MemoryStorage(),
    session=session
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

