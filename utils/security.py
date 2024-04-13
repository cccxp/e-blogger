
import re 
import bcrypt
import jwt 
import datetime

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
        'iat': datetime.datetime.now(),
        'iss': 'e-blogger',
        'data': {
            'email': email
        }
    }
    token = jwt.encode(payload, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token 


def get_current_user(token: str):
    # TODO
    pass 

