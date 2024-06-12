from database import AsyncSession
from fastapi.exceptions import HTTPException
from database_models.blog import Blog, Comment

class UseCaseBase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class AddCommentUseCase(UseCaseBase):
    async def execute(self, blog_id: int, comment_text: str, user_email: str):
        async with self.async_session() as session:
            return await Comment.add(session, blog_id, comment_text, user_email)


class GetMyCommentsUseCase(UseCaseBase):

    async def execute(self, user_email: str):
        async with self.async_session() as session:
            return await Comment.get_by_author_email(session, user_email)


class DeleteCommentUseCase(UseCaseBase):
    async def execute(self, blog_id: int, comment_id: int, user_email: str):
        async with self.async_session() as session:
            comment = await Comment.get_by_id(session, comment_id)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            if comment.author_email != user_email:
                raise HTTPException(
                    status_code=403, detail="You are not authorized to delete this blog")
            return await Comment.delete_by_id(session, comment_id)
