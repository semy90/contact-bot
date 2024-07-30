import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database.gateway import Database, ContactGateway

bot = Bot(os.getenv('TOKEN'))
contact_router = Router(name=__name__)


class FeedbackState(StatesGroup):
    waiting_contact = State()


@contact_router.callback_query(F.data == "contact_us")
async def contact_us(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="cancel"))
    await query.message.answer("Ваш отзыв будет передан администратору. Введите пожалуйста сообщение: ",
                               reply_markup=back_button.as_markup())
    await state.set_state(FeedbackState.waiting_contact)


@contact_router.message(FeedbackState.waiting_contact)
async def handle_feedback_message(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    async with session_maker() as session:
        base = Database(session)
        contact = ContactGateway(session)
        for admin in await base.get_admins():
            await bot.send_message(admin,
                                   f"Новый отзыв от @{message.from_user.username}, ID:{message.from_user.id}:\n{message.text}")
        await contact.add_application(message.from_user.id, message.from_user.username, message.text)
        await message.answer("Спасибо за отзыв! Ваше сообщение было передано администратору.")
        await state.clear()

@contact_router.callback_query(F.data == 'cancel')
async def cancel_feedback(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Отменено!')
    await state.clear()
