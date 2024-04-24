from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
import sqlalchemy
from api_models.account import *
from database_models.account import User

from utils import security
from database import AsyncSession

router = APIRouter(prefix='/account')

class UseCaseBase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class AddUser(UseCaseBase):
    async def execute(self, email: str, first_name: str, last_name: str, hashed_password: str) -> tuple[bool, str]:
        async with self.async_session.begin() as session:
            try:
                user = await User.add(session, email, first_name, last_name, hashed_password)
                return True, 'register success.'
            except sqlalchemy.exc.IntegrityError:
                return False, 'email or username already exist.'


class LoginCheck(UseCaseBase):
    async def execute(self, email: str, password: str) -> tuple[bool, str]:
        async with self.async_session.begin() as session:
            user = await User.get_by_email(session, email)
            print(user, email, password)
            if not user:
                return False, 'User not found. '
            if not security.password_validation(password, user.password):
                return False, 'Password wrong. '
            return True, 'Login success.'


class GetUserProfile(UseCaseBase):
    async def execute(self, current_user: str):
        async with self.async_session.begin() as session:
            user = await User.get_by_email(session, current_user)
            if not user:
                raise HTTPException(400, detail='User not valid.')
            return user.email, user.first_name, user.last_name, user.profile_picture, user.bio


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

