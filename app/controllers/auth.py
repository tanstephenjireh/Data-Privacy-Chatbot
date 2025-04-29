from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions.users import (InvalidCredentialsException, UserDoesNotExistException)
from app.schemas.users import Token, UserEmail, UserToken
from app.services import users as user_service
from app.utilities import password


auth_router = APIRouter()

@auth_router.post(
    "/token", response_model=Token, summary="Creates and returns a new JWT."
)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await user_service.get_by_email(form_data.username)
    if not user:
        raise UserDoesNotExistException

    if not password.verify_password(form_data.password, user["password"]):
        raise InvalidCredentialsException

    data: dict = {"sub": str(user["id"])}
    token: str = password.create_token(data)

    return {"access_token": token, "token_type": "bearer"}


@auth_router.post(
    "/token/reset-password", response_model=Token, summary="Creates and returns a new JWT for password reset."
)
async def get_reset_token(user: UserEmail):
    user = await user_service.get_by_email(user.email)

    data: dict = {"sub": str(user["id"]), "reason": "password reset"}
    token: str = password.create_token(data)

    return {"access_token": token, "token_type": "bearer"}


@auth_router.post(
    "/token/validate", response_model=UserToken, summary="Validates a JWT Token."
)
async def validate_token(token: Token):
    payload = password.decode_token(token.access_token)
    user = await user_service.get_current_user(token.access_token)
    
    return {"access_token": token.access_token, "id": user.id}
