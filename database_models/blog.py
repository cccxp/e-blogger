from .base import Base
from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from .account import User
import datetime

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_email: Mapped[str] = mapped_column(ForeignKey("users.email"))
    created_at: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="blogs")

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> "Blog":
        return (
            await session.execute(select(cls).options(joinedload(cls.author)).filter_by(id=id))
        ).scalar_one()

    @classmethod
    async def add(cls, session: AsyncSession, title: str, content: str, author_email: str) -> "Blog":
        current_time = datetime.datetime.now()
        blog = Blog(title=title, content=content, author_email=author_email, created_at=current_time, updated_at=current_time)
        session.add(blog)
        await session.commit()
        await session.refresh(blog)
        print(blog)
        return blog

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> None:
        blog = await cls.get_by_id(session, id)
        session.delete(blog)
        await session.commit()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, title: str, description: str) -> "Blog":
        current_time = datetime.datetime.now()
        blog = await cls.get_by_id(session, id)
        blog.title = title
        blog.description = description
        blog.updated_at = current_time
        await session.commit()
        await session.refresh(blog)
        return blog

    @classmethod
    async def get_all_by_author(cls, session: AsyncSession, author_email: str) -> list["Blog"]:
        return (
            await session.execute(select(cls).options(joinedload(cls.author)).filter_by(author_email=author_email))
        ).scalars().all()

