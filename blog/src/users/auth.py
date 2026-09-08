import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from database import get_db
from src.users.models import User


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me-32-bytes-min')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/users/login',
)



def hash_password(password:str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password:str):
    return password_hash.verify(password, hashed_password)



def create_access_token(username:str):
    payload = {
        'sub' : username,
        'exp': (
            datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ),


    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode( #это функция в библиотеках для работы с JSON Web Token (JWT), которая разбирает строку токена и извлекает из неё полезную нагрузку (payload)
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get('sub') # имя пользователя = из выше сделанного payload

        if username is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid token',
            )

    except jwt.ExpiredSignatureError: # истек срок токена
        raise HTTPException(
            status_code=401,
            detail='Token expired',
        )

    except jwt.InvalidTokenError: # метод decode() завершается с ошибкой, находится если провалится в класс ошибки
        raise HTTPException(
            status_code=401,
            detail='Invalid token',
        )

    user = (
        db.query(User)
        .filter(
            User.username == username,
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found',
        )

    return user












