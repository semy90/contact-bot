from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.callback_data.delete_page_factory import DelCallbackData
from bot.filters import AdminFilter
from database.gateway import ContactGateway

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

    contact = ContactGateway(session_maker())
    cur_application = await contact.get_application_by_tag(int(text))

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
