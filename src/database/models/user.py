from sqlalchemy import BigInteger, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import AlchemyBaseModel


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=False, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    is_super_admin: Mapped[bool] = mapped_column(Boolean)
