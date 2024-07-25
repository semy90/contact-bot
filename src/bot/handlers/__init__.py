from aiogram import Dispatcher

from bot.handlers.admin.admin_handler import admin_router
from bot.handlers.main_funcs.start import start_router as start_router
from bot.handlers.main_funcs.about import about_router
from bot.handlers.contact.contact import contact_router
from bot.handlers.contact.contact_panel import contact_adm_router

def include_routers(dp: Dispatcher):
    dp.include_routers(about_router)
    dp.include_routers(start_router)
    # dp.include_routers(contact_router)
    # dp.include_routers(contact_adm_router)
