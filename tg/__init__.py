from .bot import bot, dp
from .handlers import routers

# from .middlewares import DatabaseOuterMiddleware, UserMiddleware
dp.include_routers(*routers)

# dp.message.outer_middleware(DatabaseOuterMiddleware(session=session))
# dp.message.middleware(UserMiddleware())
# dp.callback_query.outer_middleware(DatabaseOuterMiddleware(session=session))
# dp.callback_query.middleware(UserMiddleware())
__all__ = ["bot", "dp"]