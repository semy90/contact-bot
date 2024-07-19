from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import AlchemyBaseModel


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=False, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean)
