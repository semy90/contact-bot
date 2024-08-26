from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.callback_data.delete_page_factory import DelCallbackData
from src.bot.callback_data.page_factory import PageCallbackData


def get_back_button() -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="cancel"))
    return back_button.as_markup()


def get_control_panel() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text="Посмотреть все заявки", callback_data=PageCallbackData(page=1).pack()))
    kb_builder.add(InlineKeyboardButton(text="Поиск заявки по номеру", callback_data='search_application'))
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data='admin'))
    return kb_builder.as_markup()

def get_search_application_back_button() -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_button.add(InlineKeyboardButton(text="Отменить", callback_data="cancel_application_send"))
    return back_button.as_markup()


def get_all_contact_back_button() -> InlineKeyboardMarkup:
    backbuttonbuilder = InlineKeyboardBuilder()
    backbuttonbuilder.add(InlineKeyboardButton(text="Назад", callback_data='contact_history'))
    return backbuttonbuilder.as_markup()