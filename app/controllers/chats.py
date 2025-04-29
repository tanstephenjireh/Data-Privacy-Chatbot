from fastapi import APIRouter, Depends
from typing import List

from app.exceptions.chats import ChatDoesNotExistException, MessageInvalidInputException
from app.exceptions.users import NotAuthorizedException
from app.schemas.chats import ChatBase, ChatRead
from app.schemas.users import UserRead
from app.schemas.messages import (
    MessageModified,
    MessageCreate,
    MessageRead,
    MessageVote,
)
from app.services import users as user_service
from app.services import chats as chat_service
from app.services import messages as message_service

# from app1.chats.schemas import ChatBase, ChatRead
# from app1.users.schemas import UserRead
# from app1.chats import services as chat_service
# from app1.users import services as user_service

chat_router = APIRouter()

""" Create new chat """


@chat_router.post("", response_model=ChatRead, summary="Create a new chat")
async def create_chat(
    chat_input: ChatBase,
    current_user: UserRead = Depends(user_service.get_current_user),
):
    chat = await chat_service.create(
        chat_input=chat_input, user_id=current_user.id, current_user=current_user
    )
    return chat


""" Get Chats by current user """


@chat_router.get(
    "", response_model=list[ChatRead], summary="Get all chats by current user"
)
async def get_chat(current_user: UserRead = Depends(user_service.get_current_user)):
    return await chat_service.get_all_by_user_id(
        user_id=current_user.id, current_user=current_user
    )


""" Get Chats by current user """


@chat_router.get(
    "/{id}", response_model=ChatRead, summary="Get all chats by current user"
)
async def get_chat_by_id(
    id: int, current_user: UserRead = Depends(user_service.get_current_user)
):
    chat: ChatRead = await chat_service.get(id, current_user=current_user)

    if chat.user_id != current_user.id:
        raise NotAuthorizedException

    return chat


@chat_router.put("/{id}", response_model=ChatRead, summary="Update a chat by id")
async def update_chat(
    id: int,
    chat_input: ChatBase,
    current_user: UserRead = Depends(user_service.get_current_user),
):
    chat = await chat_service.get(id, current_user=current_user)

    if chat.user_id != current_user.id:
        raise NotAuthorizedException

    chat = await chat_service.update(
        id, chat_input=chat_input, current_user=current_user
    )

    if chat is None:
        raise ChatDoesNotExistException

    return chat


""" Send new message """


@chat_router.post(
    "/{chat_id}/messages", response_model=MessageRead, summary="Send new message"
)
async def send_message(
    chat_id: int,
    message_input: MessageCreate,
    current_user: UserRead = Depends(user_service.get_current_user),
):
    if int(chat_id) != int(message_input.chat_id):
        raise MessageInvalidInputException

    message = await message_service.create(
        message_input=message_input, user_id=current_user.id, current_user=current_user
    )
    return message


""" Get chat messages """


@chat_router.get(
    "/{chat_id}/messages", response_model=List[MessageRead], summary="Get chat messages"
)
async def get_messages_by_chat(
    chat_id: int,
    current_user: UserRead = Depends(user_service.get_current_user),
):
    message = await message_service.get_all_by_chat_id(
        chat_id=chat_id, current_user=current_user
    )
    return message


""" Update chat message """


@chat_router.put(
    "/{chat_id}/messages/{message_id}/vote",
    response_model=MessageRead,
    summary="Vote",
)
async def vote(
    chat_id: int,
    message_id: int,
    message_input: MessageVote,
    current_user: UserRead = Depends(user_service.get_current_user),
):
    message = await message_service.vote(
        chat_id=chat_id,
        id=message_id,
        vote_input=message_input,
        current_user=current_user,
    )
    return message
