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


class GetUserProfileRequest(BaseRequestModel):
    pass


class GetUserProfileResponse(BaseResponseModel):
    email: str = Field(description="user's email, also used as primary key. ", max_length=128)
    first_name: str = Field(description="user's first name. ", max_length=64)
    last_name: str = Field(description="user's last name. ", max_length=64)
    bio: str | None = Field('', description="user's bio.")
    profile_picture: str | None = Field('', description="user's profile picture link.")


class DeleteUserResponse(BaseResponseModel):
    pass 


class UpdateProfileRequest(BaseRequestModel):
    first_name: str = Field(description="user's first name. ", max_length=64)
    last_name: str = Field(description="user's last name. ", max_length=64)
    password: str = Field('', description="user's password. leave blank if don't want to change.", max_length=64)
    bio: str = Field('', description="user's bio.")
    profile_picture: str = Field('', description="user's profile picture link.")    


class UpdateProfileResponse(BaseResponseModel):
    pass 
