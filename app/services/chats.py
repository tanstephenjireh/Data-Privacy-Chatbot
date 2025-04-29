from datetime import datetime
from pydantic import ValidationError

from app.database import database
from app.exceptions.chats import ChatDoesNotExistException
from app.exceptions.users import NotAuthorizedException
from app.schemas.chats import ChatBase, ChatRead
from app.schemas.users import UserRead
from app.models.chats import chats
from app.repositories import chats as chat_repo

async def create(chat_input: ChatBase, user_id: int, current_user: UserRead):
    
    if chat_input.status is None:
        chat_input.status = "open"
    
    if chat_input.is_hidden is None:
        chat_input.is_hidden = False

    chat_input.user_id = current_user.id
    chat_input.created_at = datetime.now()

    return await chat_repo.create(chat_input)


async def get(id: int, current_user: UserRead):
    chat = await chat_repo.get(id)
    if chat["user_id"] != current_user.id:
        raise NotAuthorizedException
    return chat


async def get_all(current_user: UserRead):
    if current_user.role != "admin":
        raise NotAuthorizedException

    return await chat_repo.get_all()

async def get_all_by_user_id(user_id: int, current_user: UserRead):
    if user_id is not current_user.id:
        raise NotAuthorizedException
    return await chat_repo.get_all_by_user_id(user_id=user_id)

async def update(id: int, chat_input: ChatBase, current_user: UserRead):
    chat: ChatRead = await chat_repo.get(id=id)

    if chat.user_id is not current_user.id:
        raise NotAuthorizedException
    
    if chat_input.status == "closed":
        chat_input.closed_at  = datetime.now()

    chat_input.created_at = chat.created_at

    return await chat_repo.update(id, chat_input)
