from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CreatedUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
