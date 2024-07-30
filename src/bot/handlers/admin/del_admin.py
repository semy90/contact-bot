from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database.gateway import Database
from aiogram.fsm.context import FSMContext

from bot.filters.admin import AdminFilter

del_router = Router(name=__name__)


class DelUserNameSate(StatesGroup):
    waiting_username = State()


@del_router.callback_query(AdminFilter(), F.data == 'del_admin')
async def del_admin(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="cancel_admin"))
    await query.message.answer("Введите username пользователя",
                               reply_markup=back_button.as_markup())
    await state.set_state(DelUserNameSate.waiting_username)


@del_router.message(AdminFilter(), DelUserNameSate.waiting_username)
async def operation_admin(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    name = message.text.replace('@', '').replace(' ', '')
    if name == message.from_user.username:
        await message.answer('Ты зачем себя удаляешь?')
        await state.clear()
        return
    async with session_maker() as session:
        base = Database(session)
        await base.del_admin(name)

    await message.answer(f"@{name} больше не Администратор :(")
    await state.clear()

@del_router.callback_query(F.data == 'cancel_admin')
async def cancel_feedback(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено!')
    await state.clear()
