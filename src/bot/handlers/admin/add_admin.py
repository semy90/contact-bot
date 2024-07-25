from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database.gateway import Database
from aiogram.fsm.context import FSMContext

from bot.filters.admin import AdminFilter

add_router = Router(name=__name__)


class AddUserNameSate(StatesGroup):
    waiting_username = State()


@add_router.callback_query(AdminFilter(), F.data == 'add_admin')
async def create_admin(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="admin"))
    await query.message.answer("Введите username пользователя",
                               reply_markup=back_button.as_markup())
    await state.set_state(AddUserNameSate.waiting_username)


@add_router.message(AdminFilter(), AddUserNameSate.waiting_username)
async def operation_admin(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    name = message.text.replace('@', '').replace(' ', '')
    async with session_maker() as session:
        base = Database(session)
        await base.make_new_admin(name)

    await message.answer(f"@{name} стал Администратором")
    await state.clear()


# @add_router.callback_query(F.data == 'admin', AdminFilter())
# async def cancel_feedback(call: CallbackQuery, state: FSMContext):
#     await call.message.answer('Отменено!')
#     await state.clear()
