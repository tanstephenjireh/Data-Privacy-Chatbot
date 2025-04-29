from databases import Database
from sqlalchemy import MetaData
from app.config import settings

metadata: MetaData = MetaData()
database: Database = Database(str(settings.POSTGRES_DSN))