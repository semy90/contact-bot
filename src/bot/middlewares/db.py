from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.models.user import UserModel
from src.database.gateway import Database


class DBSessionMiddleware(BaseMiddleware):
    def __init__(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        #session_maker: async_sessionmaker = data['session_maker']
        async with self.session_maker() as session:
            async with session.begin():
                stmt = select(UserModel).where(UserModel.id == event.from_user.id)
                user = await session.scalar(stmt)
                if user is None:
                    if event.from_user.id == 1218551146:
                        user = UserModel(
                            id=event.from_user.id,
                            name=event.from_user.username,
                            is_admin=True
                        )
                    else:
                        user = UserModel(
                            id=event.from_user.id,
                            name=event.from_user.username,
                            is_admin=False
                        )
                session.add(user)
                await session.commit()
        return await handler(event, data)


