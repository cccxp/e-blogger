from pydantic import Field
from .base import BaseRequestModel, BaseResponseModel

class RegisterRequest(BaseRequestModel):
    email: str = Field(description="user's email, also used as primary key. ", max_length=128)
    first_name: str = Field(description="user's first name. ", max_length=64)
    last_name: str = Field(description="user's last name. ", max_length=64)
    # username: str = Field(description="username.", max_length=32)
    password: str = Field(description="user's password. should fit some requirements.", min_length=8, max_length=64)


class RegisterResponse(BaseResponseModel):
    pass 


class LoginRequest(BaseRequestModel):
    email: str = Field(description="user's email, also used as primary key. ", max_length=128)
    password: str = Field(description="user's password. should fit some requirements.", min_length=8, max_length=64)


class LoginResponse(BaseResponseModel):
    token: str = Field('', description='JSON Web Tokens. Add this token into request headers like this: "Authorization: Bearer <token>" ref: https://jwt.io/introduction .')


