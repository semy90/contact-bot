from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.callback_data.delete_page_factory import DelCallbackData

from src.bot.filters import AdminFilter
from src.bot.keyboards.contact import  get_search_application_back_button
from src.bot.states.contact import CaseState
from src.database.gateway import  ContactGateway

search_router = Router(name=__name__)




@search_router.callback_query(F.data == 'search_application', AdminFilter())
async def search_application(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите номер обращения: ",
                               reply_markup=get_search_application_back_button())
    await state.set_state(CaseState.waiting)


@search_router.message(CaseState.waiting, AdminFilter())
async def handle_feedback_message(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    contact = ContactGateway(session_maker())
    text = message.text

    if not text.isdigit():
        await message.answer("Попробуйте повторно и введите ТОЛЬКО цифры")
        await state.clear()
        return

    cur_application = await contact.get_application_by_tag(int(text))

    button = InlineKeyboardBuilder()
    button.add(InlineKeyboardButton(text="Удалить", callback_data=DelCallbackData(page=0, id=int(text)).pack()))

    try:
        await message.answer(
            f"Обращение от пользователя:\n\n{cur_application['text']}\n\nНомер обращения: {cur_application['id']}\nusername : @{cur_application['username']}, ID: {cur_application['user_id']}",
            reply_markup=button.as_markup()

        )
        await state.clear()
    except TypeError:
        await message.answer(
            "Обращения не существует! Попробуйте еще раз!"
        )




@search_router.callback_query(F.data == "cancel_application_send", AdminFilter())
async def cancel_feedback(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Отменено!')
    await state.clear()
