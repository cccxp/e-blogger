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

    comments = relationship("Comment", back_populates="blog")

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> "Blog":
        return (
            await session.execute(select(cls).options(joinedload(cls.author)).filter_by(id=id))
        ).scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, title: str, content: str, author_email: str) -> "Blog":
        current_time = datetime.datetime.now()
        blog = Blog(title=title, content=content, author_email=author_email,
                    created_at=current_time, updated_at=current_time)
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

    @classmethod
    async def search_by_keywords(cls, session: AsyncSession, keywords: str, email: str) -> list["Blog"]:
        keywords = keywords.strip().lower()
        keywords = keywords.split()
        blogs = (
            await session.execute(
                select(cls).options(
                    joinedload(cls.author)
                ).filter(
                    cls.author_email == email,
                    cls.title.ilike(f'%{keywords[0]}%'),
                    cls.content.ilike(f'%{keywords[0]}%')
                ))
        ).scalars().all()
        if len(keywords) > 1:
            blogs = [
                blog for blog in blogs
                if all((
                    keyword in blog.title.lower()
                    or keyword in blog.content.lower()
                    for keyword in keywords
                ))]
        return blogs


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))
    content: Mapped[str] = mapped_column(nullable=False)
    author_email: Mapped[str] = mapped_column(ForeignKey("users.email"))
    created_at: Mapped[str] = mapped_column(nullable=False)
    
    blog: Mapped["Blog"] = relationship("Blog", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")

    @classmethod
    async def add(cls, session: AsyncSession, blog_id: int, content: str, author_email: str) -> "Comment":
        current_time = datetime.datetime.now()
        comment = Comment(blog_id=blog_id, content=content, author_email=author_email,
                          created_at=current_time, updated_at=current_time)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> None:
        comment = await cls.get_by_id(session, id)
        session.delete(comment)
        await session.commit()
