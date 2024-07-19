from aiogram import Dispatcher

from .start import start_router as start_router
from .about import about_router
from .contact import contact_router


def include_routers(dp: Dispatcher):
    dp.include_routers(start_router)
    dp.include_routers(about_router)
    dp.include_routers(contact_router)
