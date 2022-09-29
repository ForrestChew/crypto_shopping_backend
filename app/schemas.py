from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CreatedUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
