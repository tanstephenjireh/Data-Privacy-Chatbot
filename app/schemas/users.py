from passlib.hash import bcrypt
from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr, validator

class Token(BaseModel):
    access_token: str

class UserToken(BaseModel):
    id: int
    access_token: str

class UserBase(BaseModel):
    email: EmailStr
    name: str | None

class UserRegister(UserBase):
    password: SecretStr
    role: str | None
    created_at: datetime | None = datetime.now()
    updated_at: datetime | None = datetime.now()

    @validator("password", pre=True)
    def hash_password(cls, value):
        return bcrypt.hash(value)
    
class UserRead(UserBase):
    id: int
    role: str | None

class UserUpdate(BaseModel):
    email: EmailStr | None
    password: str | None
    name: str | None
    role: str | None

    @validator("password", pre=True)
    def hash_password(cls, value):
        return bcrypt.hash(value)
    
class UserEmail(BaseModel):
    email: EmailStr