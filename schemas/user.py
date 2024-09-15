from typing import Optional

from pydantic import BaseModel


class UserTokenSchema(BaseModel):
    access_token: str


class UserSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    username: str
    email: str
    disabled: bool = False


class UserUpdateSchema(UserTokenSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = False


class UserCreateSchema(UserSchema):
    password: str


class UserOutSchema(UserSchema):
    id: int

    class Config:
        from_attributes = True


class UserAuthenticateSchema(BaseModel):
    username: str
    password: str


class UserDeleteSchema(UserTokenSchema):
    password: str