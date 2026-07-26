from vkbottle import API
from vkbottle.api import ConsistentTokenGenerator

from config import VK_API1, VK_API2

token_generator = ConsistentTokenGenerator([VK_API1, VK_API2])
api = API(token_generator)
