from pydantic import Field
from .base import BaseModel, BaseRequestModel, BaseResponseModel
from .blog import ListBlogResponse


class SearchRequest(BaseRequestModel):
    query: str = Field(..., description="Search query")


class SearchResponse(ListBlogResponse):
    pass



