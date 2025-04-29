from pydantic import BaseSettings, PostgresDsn

class ApplicationSettings(BaseSettings):
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_SECONDS: int = 86400
    JWT_SECRET: str

    POSTGRES_DSN: PostgresDsn
    POSTGRES_DSN_ALEMBIC: PostgresDsn

    class Config:
        env_file: str = ".env"
        env_prefix: str = "ChatDPT_"

settings = ApplicationSettings()