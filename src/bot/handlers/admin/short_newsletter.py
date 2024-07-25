import asyncio
import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.filters import AdminFilter
from database.gateway import Database

bot = Bot(os.getenv('TOKEN'))
short_newsletter_router = Router(name=__name__)


@short_newsletter_router.message(AdminFilter(), F.text.startswith("/message"))
async def short_message(message: Message, session_maker: async_sessionmaker):
    _, *tmp = message.text.split()
    text = ' '.join(tmp)
    async with session_maker() as session:
        base = Database(session)
        user_ids = await base.get_all_users()
        for uid in user_ids:
            await bot.send_message(chat_id=uid, text=text)
            await asyncio.sleep(0.05)

    await message.answer('Рассылка завершена!')