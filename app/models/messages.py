from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import metadata

messages: Table =  Table (
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("chat_id", Integer, ForeignKey("chats.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=True),

    Column("message", String, nullable=False),
    Column("modified_message", String, nullable=True),

    Column("is_liked", Boolean),
    Column("is_disliked", Boolean),

    Column("type", String),

    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, default=datetime.now()),
    )
