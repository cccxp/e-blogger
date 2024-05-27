from typing import Annotated
from fastapi import APIRouter, Depends

from api_models.comments import *
from api_models.blog import *
# from database_usecase.comments import *

from utils.security import get_current_user

router = APIRouter(prefix='/comments')


@router.post('/{blog_id}', response_model=CreateCommentRequest)
async def add_comment(r: AddBlogRequest, user_email: str = Depends(get_current_user)):
    pass


@router.delete('/{blog_id}/{comment_id}', response_model=DeleteBlogResponse)
async def delete_blog(blog_id: int, user_email: str = Depends(get_current_user)):
    pass 
