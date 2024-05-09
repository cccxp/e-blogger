from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from api_models.blog import *
from database_models.blog import Blog

from utils.security import get_current_user
from database import AsyncSession

router = APIRouter(prefix='/blog')

class UseCaseBase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


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
                raise HTTPException(status_code=403, detail="You are not authorized to access this blog")
            return blog


class UpdateBlogUseCase(UseCaseBase):
    async def execute(self, blog_id: int, user_email: str, title: str, content: str) -> Blog:
        async with self.async_session() as session:
            blog = await Blog.get_by_id(session, blog_id)
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.author_email != user_email:
                raise HTTPException(status_code=403, detail="You are not authorized to update this blog")
            await blog.update(title, content)
            return blog


class DeleteBlogUseCase(UseCaseBase):
    async def execute(self, blog_id: int, user_email: str) -> None:
        async with self.async_session() as session:
            blog = await Blog.get_by_id(session, blog_id)
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.author_email != user_email:
                raise HTTPException(status_code=403, detail="You are not authorized to delete this blog")
            await blog.delete_by_id(session, blog_id)


@router.get('/{blog_id}', response_model=GetBlogResponse)
async def get_blog(blog_id: int, user_email: str = Depends(get_current_user), use_case: GetBlogUseCase = Depends(GetBlogUseCase)):
    blog = await use_case.execute(blog_id, user_email)
    return GetBlogResponse(success=True, message="Blog found successfully", blog=BlogModel.model_validate({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
        "author_email": blog.author_email,
    }))


@router.post('/add', response_model=AddBlogResponse)
async def add_blog(r: AddBlogRequest, user_email: str = Depends(get_current_user), use_case: AddBlogUseCase = Depends(AddBlogUseCase)):
    await use_case.execute(user_email, r.title, r.content)
    return AddBlogResponse(success=True, message="Blog added successfully")


@router.put('/{blog_id}', response_model=UpdateBlogResponse)
async def update_blog(blog_id: int, r: UpdateBlogRequest, user_email: str = Depends(get_current_user), use_case: UpdateBlogUseCase = Depends(UpdateBlogUseCase)):
    use_case.execute(blog_id, user_email, r.title, r.content)
    return UpdateBlogResponse(success=True, message="Blog updated successfully")


@router.delete('/{blog_id}', response_model=DeleteBlogResponse)
async def delete_blog(blog_id: int, user_email: str = Depends(get_current_user), use_case: DeleteBlogUseCase = Depends(DeleteBlogUseCase)):
    await use_case.execute(blog_id, user_email)
    return DeleteBlogResponse(success=True, message="Blog deleted successfully")

