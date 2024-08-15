from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.gateway import Database


class AdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return await database.admin_check(event)


class SuperAdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return await database.super_admin_check(event)
