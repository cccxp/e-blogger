from fastapi import APIRouter, Depends
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
    async def execute(self, email: str, username: str, hashed_password: str) -> tuple[bool, str]:
        async with self.async_session.begin() as session:
            try:
                user = await User.add(session, email, username, hashed_password)
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


@router.post('/register', response_model=RegisterResponse)
async def register(r: RegisterRequest, use_case: AddUser = Depends(AddUser)):
    if not security.email_check(r.email):
        return RegisterResponse(success=False, message='Email format check failed.')
    strength_check, reason = security.password_strength_check(r.password)
    if not strength_check:
        return RegisterResponse(success=False, message=f'Password strength check faild, reason: {reason}')
    # TODO: captcha check

    success, reason = await use_case.execute(r.email, r.username, security.password_encryption(r.password))
    return RegisterResponse(success=success, message=reason)


@router.post('/login', response_model=LoginResponse)
async def login(r: LoginRequest, use_case: LoginCheck = Depends(LoginCheck)):
    token = ''
    success, reason = await use_case.execute(r.email, r.password)
    if success:
        token = security.jwt_encode(r.email)
    return LoginResponse(success=success, message=reason, token=token)
