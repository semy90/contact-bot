from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import AdminFilter
from src.database.gateway import ContactGateway

del_application_router = Router(name=__name__)


@del_application_router.message(F.text.startswith('/delete'), AdminFilter())
async def del_short_application(message: Message, session: AsyncSession):
    try:
        text = message.text.split()[1]
    except IndexError:
        await message.answer("Попробуйте повторно")
        return
    if not text.isdigit():
        await message.answer("Попробуйте повторно и введите ТОЛЬКО цифры")
        return

    contact = ContactGateway(session)
    await contact.del_by_tag(int(text))
    await message.answer("Обращение удалено!")
