from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.gateway import Database
from src.database.models.user import UserModel

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start_handler(message: Message):
    menu_bulder = InlineKeyboardBuilder()
    menu_bulder.add(InlineKeyboardButton(text="О нас", callback_data='about_us'))
    menu_bulder.add(InlineKeyboardButton(text="Связаться с нами", callback_data='contact_us'))
    await message.answer('Меню бота: ',
                         reply_markup=menu_bulder.as_markup()
                         )


@start_router.callback_query(F.data == 'menu')
async def start_handler(query: CallbackQuery):
    menu_bulder = InlineKeyboardBuilder()
    menu_bulder.add(InlineKeyboardButton(text="О нас", callback_data='about_us'))
    menu_bulder.add(InlineKeyboardButton(text="Связаться с нами", callback_data='contact_us'))
    await query.message.edit_text('Меню бота: ',
                         reply_markup=menu_bulder.as_markup()
                         )





@start_router.message()
async def i_dont_understand(message: Message):
    await message.reply("Я вас не понимаю!")
