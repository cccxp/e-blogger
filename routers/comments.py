from typing import Annotated
from fastapi import APIRouter, Depends

from api_models.comments import *
from api_models.blog import *
# from database_usecase.comments import *

from utils.security import get_current_user

router = APIRouter(prefix='/comments')


@router.post('/{blog_id}', response_model=CreateCommentResponse)
async def add_comment(blog_id: int, r: CreateCommentRequest, user_email: str = Depends(get_current_user)):
    pass


@router.delete('/{blog_id}/{comment_id}', response_model=DeleteCommentResponse)
async def delete_comment(blog_id: int, comment_id: int, user_email: str = Depends(get_current_user)):
    pass 
