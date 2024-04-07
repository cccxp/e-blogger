from pydantic import Field
from .base import BaseRequestModel, BaseResponseModel

class RegisterRequest(BaseRequestModel):
    email: str = Field(description="user's email, also used as primary key. ", max_length=128)
    username: str = Field(description="username.", max_length=32)
    password: str = Field(description="user's password. should fit some requirements.", min_length=8, max_length=64)
    captcha: str = Field(description='captcha', min_length=5, max_length=5)


class RegisterResponse(BaseResponseModel):
    pass 


class LoginRequest(BaseRequestModel):
    email: str = Field(description="user's email, also used as primary key. ", max_length=128)
    password: str = Field(description="user's password. should fit some requirements.", min_length=8, max_length=64)
    captcha: str = Field(description='captcha', min_length=5, max_length=5)


class LoginResponse(BaseResponseModel):
    token: str = Field('', description='JSON Web Tokens. Add this token into request headers like this: "Authorization: Bearer <token>" ref: https://jwt.io/introduction .')


