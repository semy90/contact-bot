from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
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
        async with self.session_maker() as session:
            data['database'] = Database(session)
            data['session'] = session
            await data['database'].add_new_user(event)
        return await handler(event, data)
