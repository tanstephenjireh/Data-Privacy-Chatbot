from datetime import datetime
from pydantic import ValidationError

from app.database import database
from app.exceptions.chats import ChatDoesNotExistException
from app.exceptions.users import NotAuthorizedException
from app.schemas.chats import ChatBase, ChatRead
from app.schemas.messages import (
    MessageBase,
    MessageCreate,
    MessageModified,
    MessageVote,
)
from app.schemas.users import UserRead
from app.models.chats import chats
from app.repositories import chats as chat_repo
from app.repositories import messages as message_repo

from chatbot.chatdpt_v1 import ChatDPT, load_dpa_vector_store, load_npc_vector_store, load_flash_reranker
from app.utilities.messages import log_timing, failover, remove_failed_messages

npc_vector_store = load_npc_vector_store()
dpa_vector_store = load_dpa_vector_store()
flas_reranker = load_flash_reranker()
chatbot = ChatDPT(dpa_vector_store=dpa_vector_store, npc_vector_store=npc_vector_store, flash_reranker=flas_reranker)


# @failover
@log_timing
async def create(message_input: MessageCreate, user_id: int, current_user: UserRead):
    if user_id != current_user.id:
        raise NotAuthorizedException

    """
    ### TODO: Modify the MESSAGE PROMPT here
    """
    # DB: Save the user input message
    message_input_base = MessageModified(
        chat_id=int(message_input.chat_id),
        user_id=int(current_user.id),
        message=message_input.message,
        modified_message="",
        type="human",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_liked=0,
        is_disliked=0,
    )

    user_message = await message_repo.create(message_input_base)

    # Define ChatDPT
    # chatbot = ChatDPT()

    # Retrieve conversation history from repository
    conversation_history = await message_repo.get_all_by_chat_id(message_input.chat_id)
    conversation_history = sorted(conversation_history, key=lambda msg: msg.created_at)
    conversation_history = remove_failed_messages(conversation_history)
    # NOTE: default sort is ascending

    # Processes `conversation_history` which is a list of 
    # `app.models.messages objects` to define a `ChatMessageHistory` object
    chat_history = chatbot.preprocess_conversation_history_from_database(conversation_history)
    # Load the chat history to memory
    memory = chatbot.load_memory_with_history(chat_history)

    chatbot.initialize_conversation_chain(memory)
    # Get reply from LLM
    bot_response = chatbot.chat(message_input.message)

    # Save the reply of GPT here
    gpt_reply_message = bot_response

    message_gpt_reply = MessageModified(
        chat_id=int(message_input.chat_id),
        user_id=None,
        message=gpt_reply_message,
        modified_message=gpt_reply_message,
        type="ai",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_liked=0,
        is_disliked=0,
    )

    return await message_repo.create(message_gpt_reply)


async def get(id: int, current_user: UserRead):
    message: MessageBase = await message_repo.get(id)
    chat: ChatRead = await chat_repo.get(id=message.chat_id)
    if chat.user_id != current_user:
        raise NotAuthorizedException

    return message


async def get_all_by_chat_id(chat_id: int, current_user: UserRead):
    chat: ChatRead = await chat_repo.get(id=chat_id)
    if chat.user_id != current_user.id:
        raise NotAuthorizedException

    return await message_repo.get_all_by_chat_id(chat_id=chat.id)


async def vote(id: int, chat_id: int, vote_input: MessageVote, current_user: UserRead):
    message: MessageModified = await message_repo.get(id)

    if message.user_id is not current_user.id and message.chat_id is not chat_id:
        raise NotAuthorizedException

    message_modified = MessageModified(
        chat_id=chat_id,
        user_id=message.user_id,
        message=message.message,
        modified_message=message.modified_message,
        type=message.type,
        created_at=message.created_at,
        updated_at=datetime.now(),
        is_disliked=vote_input.is_disliked,
        is_liked=vote_input.is_liked,
    )

    print(message_modified)

    return await message_repo.update(id, message_modified)

