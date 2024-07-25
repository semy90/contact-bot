from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.bot.middlewares.db import DBSessionMiddleware


def include_middlewares(dp: Dispatcher, session_maker: async_sessionmaker):
    dp.message.outer_middleware(DBSessionMiddleware(session_maker))
    dp.callback_query.outer_middleware(DBSessionMiddleware(session_maker))

