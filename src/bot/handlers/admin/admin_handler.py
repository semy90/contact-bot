from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database.gateway import Database
from aiogram.fsm.context import FSMContext

from bot.filters.admin import AdminFilter

admin_router = Router(name=__name__)


# todo создать иерархию администраторов(одного супер админа!)

@admin_router.message(AdminFilter(), Command('admin'))
@admin_router.message(AdminFilter(), F.data == 'admin')
async def admin_menu(message: Message):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Создать админа", callback_data='add_admin'))
    kb_builder.add(InlineKeyboardButton(text="Удалить админа", callback_data='del_admin'))
    kb_builder.row(InlineKeyboardButton(text="Создать рассылку", callback_data='create_newsletter'))
    kb_builder.add(InlineKeyboardButton(text="Управление заявками", callback_data='contact_history'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='menu'))
    await message.answer("Админ-панель", reply_markup=kb_builder.as_markup(resize_keyboard=True))
