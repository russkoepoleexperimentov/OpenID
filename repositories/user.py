from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import UserModel
from schemas.user import *


class UserRepository:
    def create(self, db: Session, schema: UserCreateSchema, access_token) -> UserModel:
        user = UserModel(**schema.model_dump(), access_token=access_token)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def read(self, db: Session, user_id: int) -> UserOutSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def update(self, db: Session, schema: UserUpdateSchema, user_id: int) -> UserOutSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in schema.dict(exclude_unset=True, exclude={'access_token'}).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> UserOutSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return user

    def authenticate(self, db: Session, username: str, hashed_password: str) -> UserTokenSchema:
        user: Type[UserModel] = db.query(UserModel).filter(UserModel.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.password != hashed_password:
            raise HTTPException(status_code=403, detail="Invalid authentication data")

        return UserTokenSchema(access_token=user.access_token)

    def get_by_access_token(self, db: Session, token: str) -> UserOutSchema:
        user: Type[UserModel] = db.query(UserModel).filter(UserModel.access_token == token).first()

        if not user:
            raise HTTPException(status_code=403, detail="Invalid token")

        return user
