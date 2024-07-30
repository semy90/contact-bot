import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.filters import AdminFilter
from src.database.gateway import Database, ContactGateway

del_application_router = Router(name=__name__)

@del_application_router.message(F.text.startswith('/delete'), AdminFilter())
async def del_short_application(message: Message, session_maker: async_sessionmaker):
    _, *tmp = message.text.split()
    print(tmp)
    tag = ' '.join(tmp)

    async with session_maker() as session:
        contact = ContactGateway(session)
        await contact.del_by_tag(int(tag))
    await message.answer("Обращение удалено!")