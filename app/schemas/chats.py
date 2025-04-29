from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    name: str
    status: str | None
    is_hidden: bool | None
    user_id: int | None
    created_at: datetime | None
    closed_at: datetime | None


class ChatRead(ChatBase):
    id: int