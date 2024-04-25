import re 
import bcrypt
import jwt 
import datetime

from typing import Annotated

from fastapi import HTTPException, Header

import config

def email_check(email: str) -> bool:
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    return re.match(email_regex, email) is not None 


def password_strength_check(password: str) -> tuple[bool, str]:
    """ check if password too week. return result (boolean) and reason (string). """
    if len(password) < 8:
        return False, 'password shorter than 8 characters.'
    if len(password) > 64:
        return False, 'password too long.'
    if re.search(r'[a-z]', password, re.IGNORECASE) is None or re.search(r'[0-9]', password) is None:
        return False, 'password must contain number and alphabet.'
    return True, 'password is strong.'


def password_encryption(password: str):
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def password_validation(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def jwt_encode(email: str) -> str:
    payload = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=config.JWT_EXPIRE_TIME),
        'iss': 'e-blogger',
        'data': {
            'email': email
        }
    }
    token = jwt.encode(payload, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token 


async def get_current_user(Authorization: Annotated[str, Header()]):
    token = Authorization.replace('Bearer ', '', 1)
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM], issuer='e-blogger')
        # pyjwt will auto check issuer and exp.
        return payload['data']['email']
    except (jwt.PyJWTError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f'Token Invalid: {str(e)}')
