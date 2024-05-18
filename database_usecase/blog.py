from database_models.blog import Blog

from .base import UseCaseBase, HTTPException


class AddBlogUseCase(UseCaseBase):
    async def execute(self, user_email: str, title: str, content: str) -> Blog:
        async with self.async_session() as session:
            blog = await Blog.add(session, title, content, user_email)
            return blog


class GetBlogUseCase(UseCaseBase):
    async def execute(self, blog_id: int, email: str) -> Blog:
        async with self.async_session() as session:
            blog = await Blog.get_by_id(session, blog_id)
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.author_email != email:
                raise HTTPException(
                    status_code=403, detail="You are not authorized to access this blog")
            return blog


class UpdateBlogUseCase(UseCaseBase):
    async def execute(self, blog_id: int, user_email: str, title: str, content: str) -> Blog:
        async with self.async_session() as session:
            blog = await Blog.get_by_id(session, blog_id)
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.author_email != user_email:
                raise HTTPException(
                    status_code=403, detail="You are not authorized to update this blog")
            await blog.update(title, content)
            return blog


class DeleteBlogUseCase(UseCaseBase):
    async def execute(self, blog_id: int, user_email: str) -> None:
        async with self.async_session() as session:
            blog = await Blog.get_by_id(session, blog_id)
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.author_email != user_email:
                raise HTTPException(
                    status_code=403, detail="You are not authorized to delete this blog")
            await blog.delete_by_id(session, blog_id)


class ListBlogUseCase(UseCaseBase):
    async def execute(self, user_email: str) -> list[Blog]:
        async with self.async_session() as session:
            blogs = await Blog.get_all_by_author(session, user_email)
            return blogs
