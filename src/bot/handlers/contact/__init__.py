from aiogram import Dispatcher

from bot.handlers.contact.see_all_application import see_all_applications
from .contact import contact_router
from .contact_panel import contact_adm_router
from .search_application import search_router
from .short_del_application import del_application_router
from .short_search_application import short_search_router


def include_contact_routers(dp: Dispatcher):
    dp.include_routers(contact_router)
    dp.include_routers(contact_adm_router)
    dp.include_routers(del_application_router)
    dp.include_routers(see_all_applications)
    dp.include_routers(search_router)
    dp.include_routers(short_search_router)
