from typing import List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user import UserModel


class UserGateway:
    pass


class SubsGateway:
    pass


class ServiceGateway:
    pass


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_admins(self) -> List[int]:
        query = sa.select(UserModel).where(UserModel.is_admin == True)
        admins = await self.session.scalars(query)
        return [admin.id for admin in admins]

    async def make_new_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        user.is_admin = True
        await self.session.commit()

    async def del_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        user.is_admin = False
        await self.session.commit()



