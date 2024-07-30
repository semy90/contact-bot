from aiogram.filters.callback_data import CallbackData


class PageCallbackData(CallbackData, prefix='to'):
    page: int
