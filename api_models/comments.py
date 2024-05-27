from pydantic import Field
from .base import BaseModel, BaseRequestModel, BaseResponseModel


class Comment(BaseModel):
    id: int = Field(None, description="Comment ID")
    blog_id: int = Field(None, description="Blog ID")
    content: str = Field(None, description="Comment content")
    created_at: str = Field(None, description="Comment creation date")
    user_email: str = Field(None, description="User email")


class CreateCommentRequest(BaseRequestModel):
    blog_id: int = Field(None, description="Blog ID")
    content: str = Field(None, description="Comment content")


class CreateCommentResponse(BaseResponseModel):
    comment_id: int = Field(None, description="Comment ID")


class DeleteCommentRequest(BaseRequestModel):
    comment_id: int = Field(None, description="Comment ID")


class DeleteCommentResponse(BaseResponseModel):
    pass
