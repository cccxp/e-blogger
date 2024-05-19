from typing import Annotated
from fastapi import APIRouter, Depends

from api_models.blog import *
from api_models.search import *
from database_usecase.blog import *
from database_usecase.search import *


from utils.security import get_current_user

router = APIRouter(prefix='/blog')


@router.get('/all', response_model=ListBlogResponse)
async def get_all_blogs(user_email: str = Depends(get_current_user), use_case: ListBlogUseCase = Depends(ListBlogUseCase)):
    blogs = await use_case.execute(user_email)
    return ListBlogResponse(success=True, message="Blogs found successfully", blogs=[BlogModel.model_validate({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
        "author_email": blog.author_email,
    }) for blog in blogs])


@router.post('/search', response_model=SearchResponse)
async def search_blogs(r: SearchRequest, user_email: str = Depends(get_current_user), use_case: SearchBlogUseCase = Depends(SearchBlogUseCase)):
    blogs = await use_case.execute(r.query, user_email)
    return SearchResponse(success=True, message="Search successfully", blogs=[BlogModel.model_validate({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
        "author_email": blog.author_email,
    }) for blog in blogs])


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
