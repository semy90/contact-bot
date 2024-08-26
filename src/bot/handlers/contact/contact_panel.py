from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.filters import AdminFilter
from src.bot.keyboards.contact import get_control_panel

contact_adm_router = Router(name=__name__)


@contact_adm_router.callback_query(F.data == 'contact_history', AdminFilter())
async def control_contact_panel(query: CallbackQuery):
    await query.message.edit_text("Управление заявками:", reply_markup=get_control_panel())
