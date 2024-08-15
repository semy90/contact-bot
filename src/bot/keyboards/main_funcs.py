from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard() -> InlineKeyboardMarkup:
    menu_bulder = InlineKeyboardBuilder()
    menu_bulder.add(InlineKeyboardButton(text="О нас", callback_data='about_us'))
    menu_bulder.add(InlineKeyboardButton(text="Связаться с нами", callback_data='contact_us'))
    return menu_bulder.as_markup()