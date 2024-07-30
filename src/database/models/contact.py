from sqlalchemy import BigInteger, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AlchemyBaseModel


class ApplicationModel(AlchemyBaseModel):
    __tablename__ = "contact"
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=False, nullable=True)
    text: Mapped[str] = mapped_column(String(512), unique=False, nullable=True)

