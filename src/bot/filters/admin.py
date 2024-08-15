from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.gateway import Database
from database.models import UserModel


class AdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return await database.admin_check(event)


class SuperAdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return await database.super_admin_check(event)
