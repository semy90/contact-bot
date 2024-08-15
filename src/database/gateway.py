import os
from types import NoneType
from typing import List

import sqlalchemy as sa
from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ContactModel
from src.database.models.user import UserModel


class UserGateway:
    pass


class SubsGateway:
    pass


class ContactGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_application_by_page(self, page: int):
        query = sa.select(ContactModel)
        applications = list(await self.session.scalars(query))
        for i in range(len(applications)):
            if i == page - 1:
                application = applications[i]
                tmp_dict = {
                    'id': application.id,
                    'user_id': application.user_id,
                    'username': application.username,
                    'text': application.text
                }
                return tmp_dict

    async def del_by_tag(self, tag: int):
        query = sa.delete(ContactModel).where(tag == ContactModel.id)
        await self.session.execute(query)
        await self.session.commit()

    async def add_application(self, userid: int, username: str, text: str):
        app = ContactModel(
            user_id=userid,
            username=username,
            text=text[:512]
        )
        self.session.add(app)
        await self.session.commit()

    async def get_application_by_tag(self, tag: int):
        query = sa.select(ContactModel).where(tag == ContactModel.id)
        application = await self.session.scalar(query)
        if isinstance(application, NoneType):
            return NoneType
        tmp_dict = {
            'id': application.id,
            'user_id': application.user_id,
            'username': application.username,
            'text': application.text
        }
        return tmp_dict

    async def get_all_applications(self):
        query = sa.select(ContactModel)
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

    async def add_new_user(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(stmt)
        if user is None:
            user = UserModel(
                id=event.from_user.id,
                name=event.from_user.username,
                is_admin=(event.from_user.id == int(os.getenv('SUPER_ADMIN_ID'))),
                is_super_admin=(event.from_user.id == int(os.getenv('SUPER_ADMIN_ID'))),
            )
        self.session.add(user)

        if user.name != event.from_user.username:
            #Дополнительная проверка на смену ника у пользователя
            user.name = event.from_user.username
        await self.session.commit()

    async def super_admin_check(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.is_super_admin == 1)
        users = await self.session.scalars(stmt)
        for user in users:
            if user.id == event.from_user.id:
                return True
        return False

    async def admin_check(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.is_admin == 1)
        users = await self.session.scalars(stmt)
        for user in users:
            if user.id == event.from_user.id:
                return True
        return False




