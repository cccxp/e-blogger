from pydantic import BaseModel, Field


class BaseRequestModel(BaseModel):
    pass 

class BaseResponseModel(BaseModel):
    success: bool = Field(description='operation sucessful or not.')
    message: str = Field('', description='error message.')

