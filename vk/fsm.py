from vkbottle import BaseStateGroup, BuiltinStateDispenser
from vkbottle.tools import WaiterMachine

wm = WaiterMachine()
state_dispenser = BuiltinStateDispenser()

class SupportStates(BaseStateGroup):
    IN_SUPPORT = 0