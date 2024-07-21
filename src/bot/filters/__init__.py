from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.bot.filters.admin import AdminFilter

def include_filters(dp : Dispatcher, session_maker : async_sessionmaker):
    dp.message.filter(AdminFilter())