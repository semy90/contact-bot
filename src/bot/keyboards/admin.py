from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_create_admin_back_button() -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="add_admin_cancel"))
    return back_button.as_markup()

def get_admin_menu() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Создать админа", callback_data='add_admin'))
    kb_builder.add(InlineKeyboardButton(text="Удалить админа", callback_data='del_admin'))
    kb_builder.row(InlineKeyboardButton(text="Создать рассылку", callback_data='create_newsletter'))
    kb_builder.add(InlineKeyboardButton(text="Управление заявками", callback_data='contact_history'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='menu'))
    return kb_builder.as_markup(resize_keyboard=True)

def get_admin_menu_contact() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Создать рассылку", callback_data='create_newsletter'))
    kb_builder.add(InlineKeyboardButton(text="Управление заявками", callback_data='contact_history'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='menu'))
    return kb_builder.as_markup(resize_keyboard=True)