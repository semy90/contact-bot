from aiogram import Dispatcher

from .contact import contact_router
from .contact_panel import contact_adm_router
# from .short_del_application import del_application_router


def include_contact_routers(dp: Dispatcher):
    dp.include_routers(contact_router)
    dp.include_routers(contact_adm_router)
    # dp.include_routers(del_application_router)
