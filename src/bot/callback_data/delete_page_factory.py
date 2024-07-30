from aiogram.filters.callback_data import CallbackData


class DelCallbackData(CallbackData, prefix='to'):
    page: int
    id : int