from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from app.database import metadata

telemetry: Table =  Table (
    "telemetry",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("endpoint", String, nullable=False),
    Column("input", String, nullable=False),
    Column("start_time", DateTime, default=datetime.now()),
    Column("end_time", DateTime, default=datetime.now()),
    Column("status", String, nullable=False),
    Column("response", String, nullable=False),
    )
