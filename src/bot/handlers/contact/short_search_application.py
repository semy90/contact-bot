from types import NoneType

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.callback_data.delete_page_factory import DelCallbackData
from bot.callback_data.page_factory import PageCallbackData
from bot.filters import AdminFilter
from database.gateway import Database, ContactGateway

short_search_router = Router(name=__name__)


@short_search_router.message(F.text.startswith('/search'), AdminFilter())
async def short_search(message: Message, session_maker: async_sessionmaker):
    try:
        text = message.text.split()[1]
    except IndexError:
        await message.answer("Попробуйте повторно")
        return
    if not text.isdigit():
        await message.answer("Попробуйте повторно и введите ТОЛЬКО цифры")
        return

    app = ContactGateway(session_maker())
    cur_application = await app.get_application_by_tag(int(text))



    button = InlineKeyboardBuilder()
    button.add(InlineKeyboardButton(text="Удалить", callback_data=DelCallbackData(page=0, id=int(text)).pack()))
    try:
        await message.answer(
            f"Обращение от пользователя:\n\n{cur_application['text']}\n\nНомер обращения: {cur_application['id']}\nusername : @{cur_application['username']}, ID: {cur_application['user_id']}",
            reply_markup=button.as_markup()
        )
    except TypeError:
        await message.answer(
            "Обращения не существует!"
        )
