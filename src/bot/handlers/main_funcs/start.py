from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboards.main_funcs import get_start_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Меню бота: ',
                         reply_markup=get_start_keyboard()
                         )


@start_router.callback_query(F.data == 'menu')
async def start_handler(query: CallbackQuery):
    await query.message.edit_text('Меню бота: ',
                                  reply_markup=get_start_keyboard()
                                  )


@start_router.message()
async def i_dont_understand(message: Message):
    await message.reply("Я вас не понимаю!")
