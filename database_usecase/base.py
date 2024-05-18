from database import AsyncSession
from fastapi.exceptions import HTTPException


class UseCaseBase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session
