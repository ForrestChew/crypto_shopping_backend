from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, PositiveFloat
from typing import Optional


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    is_administrator: Optional[Boolean]


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


class CreateProduct(BaseModel):
    title: str
    category: str
    price: PositiveFloat
    quantity: int


class CreatedProduct(CreateProduct):
    id: int

    class Config:
        orm_mode = True
