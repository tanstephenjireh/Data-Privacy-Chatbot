from datetime import datetime
from pydantic import ValidationError

from app.database import database
from app.exceptions.chats import ChatDoesNotExistException
from app.schemas.chats import ChatBase, ChatRead
from app.models.chats import chats

async def create(chat_input: ChatBase):
    query = chats.insert()
    values = chat_input.dict()

    id = await database.execute(query=query, values=values)

    return {"id": id, **values}


async def get(id: int):
    query = chats.select().where(chats.c.id == id)
    return await database.fetch_one(query=query)


async def get_all():
    query = chats.select()
    return await database.fetch_all(query=query)

async def get_all_by_user_id(user_id: int):
    query = chats.select().where(chats.c.user_id == user_id)
    return await database.fetch_all(query=query)

async def update(id: int, chat_input: ChatBase):
    query = chats.update().where(chats.c.id == id)
    values = chat_input.dict()

    await database.execute(query=query, values=values)
    
    return {"id": id, **values}


async def delete(id: int) -> None:
    query = chats.delete().where(chats.c.id == id)
    await database.execute(query=query)
    
