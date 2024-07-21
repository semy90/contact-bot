from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.models import UserModel


# class AdminFilter(BaseFilter):
#     def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
#         self.session_maker = session_maker
#
#     async def __call__(self, event: TelegramObject) -> bool:
#         async with self.session_maker() as session:
#             async with session.begin():
#                 stmt = select(UserModel)
#                 users = await session.scalars(stmt)
#                 if event.from_user in users:
#                     return True
#                 print(list(users))
#                 return False

class AdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session_maker: async_sessionmaker[AsyncSession]) -> bool:
        async with session_maker() as session:
            async with session.begin():
                stmt = select(UserModel).where(UserModel.is_admin == 1)
                users = await session.scalars(stmt)
                for user in users:
                    if user.id == event.from_user.id:
                        return True
                return False