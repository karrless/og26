from vkbottle import ConsistentTokenGenerator, Bot, API, BuiltinStateDispenser
from vkbottle.tools import WaiterMachine

from config import VK_API1, VK_API2
from vk.fsm import state_dispenser
from vk.handlers import labelers

token_generator = ConsistentTokenGenerator([VK_API1, VK_API2])

api = API(token_generator)
bot = Bot(api=api, state_dispenser=state_dispenser)

for labeler in labelers:
    bot.labeler.load(labeler)

