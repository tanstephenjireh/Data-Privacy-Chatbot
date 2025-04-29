from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from app.database import metadata

users: Table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("email", String, unique=True),
    Column("role", String),
    Column("is_banned", Boolean, default=False),
    Column("password", String),
    Column("created_at",DateTime, default=datetime.now()),
    Column("updated_at",DateTime, default=datetime.now()),
)
