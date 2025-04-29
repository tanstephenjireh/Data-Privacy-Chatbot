from asyncpg.exceptions import UniqueViolationError
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from passlib.hash import bcrypt
from pydantic import ValidationError
from typing import Any

from app.database import database
from app.exceptions.users import UserDoesNotExistException, UserExistsException
from app.models.users import users
from app.schemas.users import UserRead, UserRegister, UserUpdate

import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def create(user_input: UserRegister):
    query = users.insert()
    values = user_input.dict()
    values.update({"password": user_input.password.get_secret_value()})
    id = await database.execute(query=query, values=values)

    return {"id": id, **values}

async def get(id: int):
    query = users.select().where(users.c.id == id)
    return await database.fetch_one(query=query)


async def get_all():
    query = users.select()
    return await database.fetch_all(query=query)

async def get_by_email(email: str):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query=query)

async def update(id: int, user_input: UserUpdate):
    try:
        stored_user = UserRead.parse_obj(await get(id=id))
    except ValidationError:
        raise UserDoesNotExistException
    
    updated_data = user_input.dict(exclude_unset=True)
    updated_user = stored_user.copy(update=updated_data)

    query = users.update().where(users.c.id == id)
    values = updated_user.dict()

    try:
        await database.execute(query=query, values=values)
    except UniqueViolationError:
        raise UserExistsException
    
    return updated_user


async def delete(id: int) -> None:
    query = users.delete().where(users.c.id == id)

    await database.execute(query=query)