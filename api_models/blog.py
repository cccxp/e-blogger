from pydantic import Field
from .base import BaseModel, BaseRequestModel, BaseResponseModel


class BlogModel(BaseModel):
    id: int = Field(None, description="Blog ID")
    title: str = Field(None, description="Blog Title")
    content: str = Field(None, description="Blog Content")
    created_at: str = Field(None, description="Blog Created At")
    updated_at: str = Field(None, description="Blog Updated At")
    author_email: str = Field(None, description="Blog Author Email")


class GetUserBlogsRequest(BaseRequestModel):
    pass 


class GetUserBlogsResponse(BaseResponseModel):
    blogs: list[BlogModel] = Field(None, description="List of blogs")


class GetBlogResponse(BaseResponseModel):
    blog: BlogModel = Field(None, description="Blog Details")


class AddBlogRequest(BaseRequestModel):
    title: str = Field(None, description="Blog Title")
    content: str = Field(None, description="Blog Content")
    

class AddBlogResponse(BaseResponseModel):
    pass 


class UpdateBlogRequest(BaseRequestModel):
    title: str = Field(None, description="Blog Title")
    content: str = Field(None, description="Blog Content")


class UpdateBlogResponse(BaseResponseModel):
    pass 


class DeleteBlogResponse(BaseResponseModel):
    pass 


class ListBlogResponse(BaseResponseModel):
    blogs: list[BlogModel] = Field(None, description="List of blogs")
