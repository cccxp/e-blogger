from fastapi import APIRouter
from api_models.account import *


router = APIRouter(prefix='/account')

@router.post('/register', response_model=RegisterResponse)
def register(r: RegisterRequest):
    pass


@router.post('/login', response_model=LoginResponse)
def login(r: LoginRequest):
    pass 
