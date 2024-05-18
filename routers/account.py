from typing import Annotated
from fastapi import APIRouter, Depends

from api_models.account import *
from database_usecase.account import *

from utils import security

router = APIRouter(prefix='/account')


@router.post('/register', response_model=RegisterResponse)
async def register(r: RegisterRequest, use_case: AddUser = Depends(AddUser)):
    if not security.email_check(r.email):
        return RegisterResponse(success=False, message='Email format check failed.')
    strength_check, reason = security.password_strength_check(r.password)
    if not strength_check:
        return RegisterResponse(success=False, message=f'Password strength check faild, reason: {reason}')
    success, reason = await use_case.execute(r.email, r.first_name, r.last_name, security.password_encryption(r.password))
    return RegisterResponse(success=success, message=reason)


@router.post('/login', response_model=LoginResponse)
async def login(r: LoginRequest, use_case: LoginCheck = Depends(LoginCheck)):
    token = ''
    success, reason = await use_case.execute(r.email, r.password)
    if success:
        token = security.jwt_encode(r.email)
    return LoginResponse(success=success, message=reason, token=token)


@router.get("/profile/me", response_model=GetUserProfileResponse)
async def get_profile(current_user: str = Depends(security.get_current_user), use_case: GetUserProfile = Depends(GetUserProfile)):
    email, first_name, last_name, profile_picture, bio = await use_case.execute(current_user)
    return GetUserProfileResponse(success=True, message='', email=email, first_name=first_name, last_name=last_name, bio=bio, profile_picture=profile_picture)


@router.delete("/profile/me", response_model=DeleteUserResponse)
async def delete_account(current_user: str = Depends(security.get_current_user), use_case: DeleteUser = Depends(DeleteUser)):
    await use_case.execute(current_user)
    return DeleteUserResponse(success=True, message='delete successful.')


@router.put("/profile/me", response_model=UpdateProfileResponse)
async def update_profile(r: UpdateProfileRequest, current_user: str = Depends(security.get_current_user), use_case: UpdateUserProfile = Depends(UpdateUserProfile)):
    await use_case.execute(current_user, r.password, r.first_name, r.last_name, r.profile_picture, r.bio)
    return UpdateProfileResponse(success=True, message='update successful.')
