from typing import Any, Dict

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.database.models.base import AlchemyBaseModel

__all__ = (
    "AlchemyBaseModel",
    "init_db",
)


async def init_db(settings: Dict[str, Any]) -> async_sessionmaker:
    async_engine = create_async_engine(f"sqlite+aiosqlite:///{settings['path']}")

    async with async_engine.begin() as conn:
        #await conn.run_sync(AlchemyBaseModel.metadata.drop_all)
        await conn.run_sync(AlchemyBaseModel.metadata.create_all)

    return async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
        expire_on_commit=False,
    )
