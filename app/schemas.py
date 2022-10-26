from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, PositiveFloat
from typing import Optional


class UserIn(BaseModel):
    email: EmailStr
    password: str
    is_administrator: Optional[Boolean]


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Tokens(BaseModel):
    access_token: str
    refresh_token: Optional[str]


class ProductIn(BaseModel):
    title: str
    category: str
    description: str
    price: PositiveFloat
    quantity: int
    image_title: Optional[str]
    is_top_deal: Boolean


class ProductOut(ProductIn):
    id: int

    class Config:
        orm_mode = True


class ProductCreate(ProductIn):
    class Config:
        orm_mode = True


class SearchResults(BaseModel):
    id: int
    title: str
    category: str

    class Config:
        orm_mode = True


class CartIn(BaseModel):
    user_id: int
    cart_quantity: Optional[int]


class CartOut(CartIn):
    id: int
    cart_quantity: Optional[int]

    class Config:
        orm_mode = True
