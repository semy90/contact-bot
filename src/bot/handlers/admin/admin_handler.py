from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.bot.keyboards.admin import get_admin_menu, get_admin_menu_contact
from src.bot.filters.admin import AdminFilter, SuperAdminFilter

admin_router = Router(name=__name__)


@admin_router.message(SuperAdminFilter(), Command('admin'))
async def admin_menu(message: Message):
    await message.answer(
        "Админ-панель\n\n/message <текст рассылки> - Для быстрой рассылки сообщений\n/delete <номер обращения> - Для удаления заявки\n/search <номер обращения> - Для просмотра обращения",
        reply_markup=get_admin_menu())


@admin_router.callback_query(SuperAdminFilter(), F.data == 'admin')
async def admin_menu(query: CallbackQuery):
    await query.message.edit_text(
        "Админ-панель\n\n/message <текст рассылки> - Для быстрой рассылки сообщений\n/delete <номер обращения> - Для удаления заявки\n/search <номер обращения> - Для просмотра обращения",
        reply_markup=get_admin_menu())


@admin_router.message(AdminFilter(), Command('admin'))
async def admin_menu_contact(message: Message):
    await message.answer(
        "Админ-панель\n\n/message <текст рассылки> - Для быстрой рассылки сообщений\n/delete <номер обращения> - Для удаления заявки\n/search <номер обращения> - Для просмотра обращения",
        reply_markup=get_admin_menu_contact())


@admin_router.callback_query(AdminFilter(), F.data == 'admin')
async def admin_menu_contact(query: CallbackQuery):
    await query.message.edit_text(
        "Админ-панель\n\n/message <текст рассылки> - Для быстрой рассылки сообщений\n/delete <номер обращения> - Для удаления заявки\n/search <номер обращения> - Для просмотра обращения",
        reply_markup=get_admin_menu_contact())
