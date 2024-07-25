from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.filters import AdminFilter

contact_adm_router = Router(name=__name__)

@contact_adm_router.callback_query(F.data == 'contact_history', AdminFilter())
async def get_contact_panel(query : CallbackQuery):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Посмотреть все заявки", callback_data='see_all_applications'))
    kb_builder.add(InlineKeyboardButton(text="Поиск заявки по нику", callback_data='see_application_from_user'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='admin'))
    kb_builder.add(InlineKeyboardButton(text="Поиск заявки по тегу", callback_data='search_application'))
    await query.message.edit_text("Управление заявками:", reply_markup=kb_builder.as_markup())