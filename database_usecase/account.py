from sqlalchemy.exc import IntegrityError

from utils import security
from .base import UseCaseBase, HTTPException
from database_models.account import User


class AddUser(UseCaseBase):
    async def execute(self, email: str, first_name: str, last_name: str, hashed_password: str) -> tuple[bool, str]:
        async with self.async_session.begin() as session:
            try:
                user = await User.add(session, email, first_name, last_name, hashed_password)
                return True, 'register success.'
            except IntegrityError:
                return False, 'email or username already exist.'


class LoginCheck(UseCaseBase):
    async def execute(self, email: str, password: str) -> tuple[bool, str]:
        async with self.async_session.begin() as session:
            user = await User.get_by_email(session, email)
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


class UpdateUserProfile(UseCaseBase):
    async def execute(self, current_user: str, password: str, first_name: str, last_name: str, profile_picture: str, bio: str):
        async with self.async_session.begin() as session:
            if password:
                password = security.password_encryption(password)
            user = await User.update(session, current_user, first_name, last_name, password, bio, profile_picture)
            return user


class DeleteUser(UseCaseBase):
    async def execute(self, current_user: str):
        async with self.async_session.begin() as session:
            user = await User.get_by_email(session, current_user)
            if not user:
                raise HTTPException(400, detail='User not valid.')
            await User.delete(session, user)
