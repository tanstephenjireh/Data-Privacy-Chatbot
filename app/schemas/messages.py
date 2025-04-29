from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    chat_id: int
    user_id: int | None
    message: str


class MessageBase(MessageCreate):
    type: str | None

    is_liked: bool | None
    is_disliked: bool | None

    created_at: datetime | None
    updated_at: datetime | None


class MessageVote(BaseModel):
    is_liked: bool | None
    is_disliked: bool | None


class MessageModified(MessageBase):
    modified_message: str


class MessageRead(MessageBase):
    id: int


class MessageReadAll(MessageRead, MessageModified):
    pass
