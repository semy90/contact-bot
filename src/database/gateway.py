from types import NoneType
from typing import List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ApplicationModel
from src.database.models.user import UserModel


class UserGateway:
    pass


class SubsGateway:
    pass


class ContactGateway:
    def __init__(self, session: AsyncSession):
        self.session = session



    async def del_by_tag(self, tag : int):
        query = sa.delete(ApplicationModel).where(tag == ApplicationModel.id)
        await self.session.execute(query)
        await self.session.commit()

    async def add_application(self, userid: int, username: str, text: str):
        app = ApplicationModel(
            user_id=userid,
            username=username,
            text=text[:512]
        )
        self.session.add(app)
        await self.session.commit()

    async def get_application_by_tag(self, tag: int):
        query = sa.select(ApplicationModel).where(tag == ApplicationModel.id)
        application = await self.session.scalar(query)
        tmp_dict = {
            'id': application.id,
            'user_id': application.user_id,
            'username': application.username,
            'text': application.text
        }
        return tmp_dict

    async def get_all_applications(self):
        query = sa.select(ApplicationModel)
        applications = await self.session.scalars(query)
        all_application = []
        for application in applications:
            tmp_dict = {
                'id': application.id,
                'user_id': application.user_id,
                'username': application.username,
                'text': application.text
            }
            all_application.append(tmp_dict)
        return all_application


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> List[int]:
        query = sa.select(UserModel)
        users = await self.session.scalars(query)
        return [user.id for user in users]

    async def get_admins(self) -> List[int]:
        query = sa.select(UserModel).where(UserModel.is_admin == True)
        admins = await self.session.scalars(query)
        return [admin.id for admin in admins]

    async def make_new_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        if isinstance(user, UserModel):
            user.is_admin = True
            await self.session.commit()

    async def del_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        if isinstance(user, UserModel):
            user.is_admin = False
            await self.session.commit()
