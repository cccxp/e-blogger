from database_models.blog import Blog

from .base import UseCaseBase, HTTPException


class SearchBlogUseCase(UseCaseBase):
    async def execute(self, query: str, email: str) -> Blog:
        async with self.async_session() as session:
            blogs = await Blog.search_by_keywords(session, query, email)
            return blogs
