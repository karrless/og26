from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    storage=MemoryStorage(),
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

