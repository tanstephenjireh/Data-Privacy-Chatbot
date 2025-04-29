from asyncpg.exceptions import UniqueViolationError
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from passlib.hash import bcrypt
from pydantic import ValidationError
from typing import Any

import uuid

from app.config import settings
from app.exceptions.users import NotAuthenticatedException



def verify_password(
    password: str,
    hash: str
) -> bool: 
    return bcrypt.verify(password, hash)


def create_token(
    data: dict[str, Any]
) -> str:
    "Create a JWT Token"
    exp = datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_SECONDS)
    data.update({"exp": exp, "jti": str(uuid.uuid4())})

    return jwt.encode(
        claims=data,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_token(token: str) -> dict[str, Any]:
    "Decode a JWT Token"

    try:
        data = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM
        )
    except ExpiredSignatureError:
        raise NotAuthenticatedException
    
    return data