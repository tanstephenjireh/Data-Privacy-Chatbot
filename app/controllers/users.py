from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions.users import UserExistsException, UserDoesNotExistException, NotAuthorizedException
from app.schemas.users import UserRead, UserRegister, UserUpdate
from app.services import users as user_service


user_router = APIRouter()

""" Create new user"""
@user_router.post(
    "", 
    response_model=UserRead, 
    summary="Create a new user"
)
async def create_user(
    user_input: UserRegister
):
    if await user_service.user_exists(
        email=user_input.email
    ):
        raise UserExistsException
    user_input.role = "default"
    user_input.created_at = datetime.now()
    user_input.updated_at = datetime.now()
    user = await user_service.create(user_input=user_input)
    return user

""" Get current user """
@user_router.get(
    "/me", 
    response_model=UserRead, 
    summary="Return the current user."
)
async def read_current_user(
    user: UserRead = Depends(user_service.get_current_user)
):
    return user

""" Get current user """
@user_router.get(
    "", 
    response_model=list[UserRead], 
    summary="Return all users."
)
async def read_all_user(
    user: UserRead = Depends(user_service.get_current_user)
):
    if user.role != "admin":
        raise NotAuthorizedException 
    return await user_service.get_all()

""" Update current user """
@user_router.put(
    "/me", 
    response_model=UserRead, 
    summary="Updates the current user."
)
async def update_current_user(
    user_in: UserUpdate, 
    current_user: UserRead = Depends(user_service.get_current_user)
):
    user = await user_service.update(current_user.id, user_in)

    return user

""" Get user by id"""
@user_router.get("/{id}", response_model=UserRead, summary="Returns a user by ID.")
async def read_user(
    id: int,
    current_user: UserRead = Depends(user_service.get_current_user)
):
    user = await user_service.get(id)
    
    if current_user.id != id and current_user.role != "admin":
        raise NotAuthorizedException

    if user is None:
        raise UserDoesNotExistException

    return user

""" Update user """
@user_router.put(
    "/{id}", 
    response_model=UserRead, 
    summary="Updates a user by ID."
)
async def update_user(
    id: int, 
    user_in: UserUpdate,
    current_user: UserRead = Depends(user_service.get_current_user)
):
    if current_user.id != id and current_user.role != "admin":
        raise NotAuthorizedException

    user = await user_service.update(id, user_in)
    
    if user is None:
        raise UserDoesNotExistException

    return user