from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from .start import router

about_router = Router(name=__name__)

@about_router.callback_query(F.data == 'about_us')
async def about_us(query: CallbackQuery):
    social_networks = InlineKeyboardBuilder()
    social_networks.add(InlineKeyboardButton(text="Youtube", url='youtube.com'))
    social_networks.add(InlineKeyboardButton(text="VK", url='vk.ru'))
    social_networks.row(InlineKeyboardButton(text="Назад", callback_data="menu"))
    social_networks.add(InlineKeyboardButton(text="Telegram channel", url='telegram.org'))
    await query.message.edit_text("Мы - компания страховщиков, кайфуем с своего дела и тд.\nНаши соц.сети:",
                               reply_markup=social_networks.as_markup())
