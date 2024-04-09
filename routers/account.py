from fastapi import APIRouter, Depends
from api_models.account import *
from database_models.account import User

from utils import security
from database import AsyncSession

router = APIRouter(prefix='/account')

class AddUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, email: str, username: str, hashed_password: str) -> None:
        async with self.async_session.begin() as session:
            user = await User.add(session, email, username, hashed_password)


@router.post('/register', response_model=RegisterResponse)
async def register(r: RegisterRequest, use_case: AddUser = Depends(AddUser)):
    if not security.email_check(r.email):
        return RegisterResponse(success=False, message='Email format check failed.')
    strength_check, reason = security.password_strength_check(r.password)
    if not strength_check:
        return RegisterResponse(success=False, message=f'Password strength check faild, reason: {reason}')
    # TODO: captcha check

    await use_case.execute(r.email, r.username, security.password_encryption(r.password))
    return RegisterResponse(success=True, message='register sucess.')


@router.post('/login', response_model=LoginResponse)
async def login(r: LoginRequest):
    pass 
