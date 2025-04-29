from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, DateTime
from app.database import metadata

chats: Table =  Table (
    "chats",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("status", String),
    Column("is_hidden", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("closed_at", DateTime),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)
