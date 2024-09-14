from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: str
    email: str
    disabled: bool


class UserUpdateSchema(BaseModel):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserCreateSchema(UserSchema):
    password: str


class UserModelSchema(UserCreateSchema):
    id: int

    class Config:
        from_attributes = True