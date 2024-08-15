import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import  AsyncSession

from bot.filters import AdminFilter
from bot.states.admin import CreateNewsLetterState
from database.gateway import Database
from utils.sender import send_preview, start_sender

bot = Bot(os.getenv("TOKEN"))
newsletter_router = Router(name=__name__)



@newsletter_router.callback_query(AdminFilter(), F.data == 'create_newsletter')
async def create_sender(query: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="cancel_admin"))
    await query.message.answer('Введите текст рассылки', keyboard=back_button.as_markup())
    await state.set_state(CreateNewsLetterState.get_text)


@newsletter_router.message(AdminFilter(), F.text, CreateNewsLetterState.get_text)
async def set_text(message: Message, state: FSMContext):
    await state.update_data(msg_text=message.text)
    await message.answer("Прекрасно, прешлите теперь фото!")
    await state.set_state(CreateNewsLetterState.get_photo)


@newsletter_router.message(AdminFilter(), F.photo, CreateNewsLetterState.get_photo)
async def set_photo(message: Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer("Отлично, теперь прешлите текст для кнопки!")
    await state.set_state(CreateNewsLetterState.get_kb_text)


@newsletter_router.message(AdminFilter(), F.text, CreateNewsLetterState.get_kb_text)
async def set_kb(message: Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await message.answer("Окей!, отправьте url для кнопки!")
    await state.set_state(CreateNewsLetterState.get_kb_url)


@newsletter_router.message(AdminFilter(), F.text, CreateNewsLetterState.get_kb_url)
async def set_kb(message: Message, state: FSMContext):
    build = InlineKeyboardBuilder()
    build.row(
        InlineKeyboardButton(text='Отправить сейчас', callback_data='sent_now'),
        InlineKeyboardButton(text='Отменить', callback_data='cancel_now')

    )
    await state.update_data(btn_url=message.text)
    data = await state.get_data()
    message_id = await send_preview(
        message,
        data
    )
    await state.update_data(message_id=message_id)
    await message.answer(
        text='Сообщение сформировано',
        reply_markup=build.as_markup(),
    )
    await  state.set_state(CreateNewsLetterState.confirm_state)


@newsletter_router.callback_query(AdminFilter(), F.data == 'cancel_now', CreateNewsLetterState.confirm_state)
async def cancel_send(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Рассылка отменена')
    await state.clear()
    await query.answer()


@newsletter_router.callback_query(AdminFilter(), F.data == "sent_now", CreateNewsLetterState.confirm_state, )
async def confirm_send( query: CallbackQuery,state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await query.message.answer('Рассылка началась')
    await state.clear()
    await query.answer()

    message_id = data.get('message_id')

    base = Database(session)
    user_ids = await base.get_all_users()
    count = await start_sender(
        session=session,
        bot=bot,
        data=data,
        user_ids=user_ids,
        from_chat_id=query.message.chat.id,
        message_id=message_id
    )
    await query.message.answer(f'Отправлено {count} сообщений')
