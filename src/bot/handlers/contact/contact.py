import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.callback_data.delete_page_factory import DelCallbackData
from src.bot.keyboards.contact import get_back_button
from src.bot.states.contact import ContactState
from src.database.gateway import Database, ContactGateway

bot = Bot(os.getenv('TOKEN'))
contact_router = Router(name=__name__)


@contact_router.callback_query(F.data == "contact_us")
async def contact_us(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Ваше обращение будет передано администратору. Введите пожалуйста обращение: ",
                               reply_markup=get_back_button())
    await state.set_state(ContactState.waiting_contact)


@contact_router.message(ContactState.waiting_contact)
async def handle_feedback_message(message: Message, state: FSMContext, session: AsyncSession):
    """Хендлер отвечающий за обработку и добавление новых обращений"""

    contact = ContactGateway(session)
    base = Database(session)

    await contact.add_application(message.from_user.id, message.from_user.username, message.text)

    all_message = await contact.get_all_applications()
    cur_mes = all_message[-1]

    button = InlineKeyboardBuilder()
    button.add(
        InlineKeyboardButton(text="Удалить", callback_data=DelCallbackData(page=0, id=int(cur_mes['id'])).pack()))
    await message.answer("Спасибо за заявку! Ваше обращение было передано администратору.")

    for admin in await base.get_admins():
        await bot.send_message(admin,
                               f"Новое обращение от @{cur_mes['username']}, ID:{cur_mes['user_id']}, ID заявки: {cur_mes['id']}\n\n{cur_mes['text']}",
                               reply_markup=button.as_markup())
    await state.clear()


@contact_router.callback_query(F.data == 'cancel')
async def cancel_feedback(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Отменено!')
    await state.clear()
