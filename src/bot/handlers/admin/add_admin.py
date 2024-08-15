from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.keyboards.admin import get_create_admin_back_button
from bot.states.admin import AddUserNameState
from src.database.gateway import Database
from aiogram.fsm.context import FSMContext

from bot.filters.admin import AdminFilter, SuperAdminFilter

add_router = Router(name=__name__)




@add_router.callback_query(SuperAdminFilter(), F.data == 'add_admin')
async def create_admin(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите username пользователя",
                               reply_markup=get_create_admin_back_button())
    await state.set_state(AddUserNameState.waiting_username)


@add_router.message(SuperAdminFilter(), AddUserNameState.waiting_username)
async def operation_admin(message: Message, state: FSMContext, session: AsyncSession):
    name = message.text.replace('@', '').replace(' ', '')
    if name == message.from_user.username:
        await message.answer('Ты зачем себя добавляешь?')
        await state.clear()
        return

    base = Database(session)
    await base.make_new_admin(name)

    await message.answer(f"@{name} стал Администратором")
    await state.clear()


@add_router.callback_query(F.data == 'add_admin_cancel', SuperAdminFilter())
async def cancel_feedback(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено!')
    await state.clear()
