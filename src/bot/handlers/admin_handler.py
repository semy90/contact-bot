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

#todo создать иерархию администраторов(одного супер админа!)


class AddUserNameSate(StatesGroup):
    waiting_username = State()


class DelUserNameSate(StatesGroup):
    waiting_username = State()


@admin_router.message(AdminFilter(), Command('admin'))
@admin_router.message(AdminFilter(), F.data == 'admin')
async def admin_menu(message: Message):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Создать админа", callback_data='add_admin'))
    kb_builder.add(InlineKeyboardButton(text="Удалить админа", callback_data='del_admin'))
    kb_builder.row(InlineKeyboardButton(text="Создать рассылку", callback_data='create_newsletter'))
    kb_builder.add(InlineKeyboardButton(text="Создать пост", callback_data='create_post'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='menu'))
    await message.answer("Админ-панель", reply_markup=kb_builder.as_markup(resize_keyboard=True))


@admin_router.callback_query(AdminFilter(), F.data == 'add_admin')
async def create_admin(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="admin"))
    await query.message.answer("Введите username пользователя",
                               reply_markup=back_button.as_markup())
    await state.set_state(AddUserNameSate.waiting_username)


@admin_router.message(AdminFilter(), AddUserNameSate.waiting_username)
async def operation_admin(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    name = message.text.replace('@', '').replace(' ', '')
    async with session_maker() as session:
        base = Database(session)
        await base.make_new_admin(name)

    await message.answer(f"@{name} стал Администратором")
    await state.clear()


@admin_router.callback_query(AdminFilter(), F.data == 'del_admin')
async def del_admin(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="admin"))
    await query.message.answer("Введите username пользователя",
                               reply_markup=back_button.as_markup())
    await state.set_state(DelUserNameSate.waiting_username)


@admin_router.message(AdminFilter(), DelUserNameSate.waiting_username)
async def operation_admin(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    name = message.text.replace('@', '').replace(' ', '')
    async with session_maker() as session:
        base = Database(session)
        await base.del_admin(name)

    await message.answer(f"@{name} больше не Администратор :(")
    await state.clear()


@admin_router.callback_query(F.data == 'admin')
async def cancel_feedback(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено!')
    await state.clear()
