from datetime import datetime
from pydantic import ValidationError

from app.database import database
from app.schemas.messages import MessageBase, MessageModified
from app.models.messages import messages

async def create(message_input: MessageBase):
    query = messages.insert()
    values = message_input.dict()

    id = await database.execute(query=query, values=values)

    return {"id": id, **values}

async def get(id: int):
    query = messages.select().where(messages.c.id == id)
    return await database.fetch_one(query=query)

async def get_all(): # TODO: Pagination
    query = messages.select()
    return await database.fetch_all(query=query)

async def get_all_by_chat_id(chat_id: int):
    query = messages.select().where(messages.c.chat_id == chat_id)
    return await database.fetch_all(query=query)

async def update(id: int, message_input: MessageModified):
    query = messages.update().where(messages.c.id == id)
    values = message_input.dict()

    await database.execute(query=query, values=values)
    
    return {"id": id, **values}

async def delete(id: int) -> None:
    query = messages.delete().where(messages.c.id == id)
    await database.execute(query=query)