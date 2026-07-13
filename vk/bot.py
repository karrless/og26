from vkbottle import ConsistentTokenGenerator, Bot, API, BuiltinStateDispenser

from config import VK_API1, VK_API2

# from og_bots.bot.handlers import labelers

token_generator = ConsistentTokenGenerator([VK_API1, VK_API2])

api = API(token_generator)
state_dispenser = BuiltinStateDispenser()
bot = Bot(api=api, state_dispenser=state_dispenser)

# for labeler in labelers:
#     bot.labeler.load(labeler)


