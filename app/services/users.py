from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.users import InvalidCredentialsException, UserDoesNotExistException, UserExistsException
from app.models.users import users
from app.repositories import users as user_repo # import get, get_by_email, create, update, delete
from app.schemas.users import UserUpdate, UserRegister
from app.utilities.password import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    id = int(payload.get("sub"))

    if id is None:
        raise InvalidCredentialsException
    
    user = await user_repo.get(id=id)

    if user is None:
        raise UserDoesNotExistException
    
    return user

async def create(user_input: UserRegister):
    return await user_repo.create(user_input=user_input)

async def get(id: int):
    return await user_repo.get(id)

async def get_all():
    return await user_repo.get_all()

async def get_by_email(email: str):
    return await user_repo.get_by_email(email=email)

async def update(id: int, user_input: UserUpdate):
    return await user_repo.update(id=id, user_input=user_input)

async def delete(id: int):
    return await user_repo.delete(id=id)



""" ------- Check ------- """

async def user_exists(email: str) -> bool:
    """Checks if a user exists given a username or email."""
    return await user_repo.get_by_email(email)