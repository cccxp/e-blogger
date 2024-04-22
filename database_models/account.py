from .base import Base
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        "email", nullable=False, unique=True, primary_key=True
    )
    password: Mapped[str] = mapped_column(
        "password", nullable=False,
    )
    username: Mapped[str] = mapped_column(
        "username", nullable=True,
    )
    first_name: Mapped[str] = mapped_column(
        "first_name", nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        "last_name", nullable=True,
    )
    profile_picture: Mapped[str] = mapped_column(
        "profile_picture", nullable=True,
    )
    bio: Mapped[str] = mapped_column(
        "bio", nullable=True,
    )
    

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str):
        stmt = select(cls).where(cls.email == email)
        return await session.scalar(stmt)

    @classmethod
    async def add(cls, session: AsyncSession, email: str, first_name: str, last_name: str, password: str):
        user = User(email=email, first_name=first_name, last_name=last_name, password=password)
        session.add(user)
        await session.flush()

        new = await cls.get_by_email(session, email)
        if not new:
            raise RuntimeError('user add failed')
        return new 
    

