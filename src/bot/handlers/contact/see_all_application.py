from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from bot.callback_data.delete_page_factory import DelCallbackData
from bot.callback_data.page_factory import PageCallbackData
from bot.filters import AdminFilter
from bot.keyboards.contact import get_all_contact_back_button
from database.gateway import ContactGateway
from database.models import ContactModel

see_all_applications = Router(name=__name__)


@see_all_applications.callback_query(PageCallbackData.filter(), AdminFilter())
async def see_all_apps(query: CallbackQuery, session: AsyncSession, callback_data: PageCallbackData):
    cur = int(str(callback_data).split('=')[1])

    contact = ContactGateway(session)
    result = await session.execute(select(func.count()).where(ContactModel.id))
    count_pages = result.scalar()

    if count_pages == 0:
        await query.message.edit_text("Нет обращений!", reply_markup=get_all_contact_back_button())
        return

    if cur < 1:
        cur = count_pages
    if cur > count_pages:
        cur = 1

    cur_application = await contact.get_application_by_page(cur)

    kb_bulder = InlineKeyboardBuilder()
    kb_bulder.add(InlineKeyboardButton(text="<-", callback_data=PageCallbackData(page=cur - 1).pack()))
    kb_bulder.add(InlineKeyboardButton(text=f"{cur}/{count_pages}", callback_data='None'))
    kb_bulder.add(InlineKeyboardButton(text="->", callback_data=PageCallbackData(page=cur + 1).pack()))
    kb_bulder.row(InlineKeyboardButton(text="Назад", callback_data='contact_history'))
    kb_bulder.add(
        InlineKeyboardButton(text="del", callback_data=DelCallbackData(page=cur, id=cur_application['id']).pack()))

    await query.message.edit_text(
        f"Обращение от пользователя:\n\n{cur_application['text']}\n\nНомер обращения: {cur_application['id']}\nusername : @{cur_application['username']}, ID: {cur_application['user_id']}"
        , reply_markup=kb_bulder.as_markup())


@see_all_applications.callback_query(DelCallbackData.filter(), AdminFilter())
async def del_cur_application(query: CallbackQuery, session: AsyncSession, callback_data: DelCallbackData):
    contact = ContactGateway(session)
    await contact.del_by_tag(callback_data.id)
    await query.message.edit_text('Обращение удалено!', reply_markup=get_all_contact_back_button())
