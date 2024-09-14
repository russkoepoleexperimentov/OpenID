from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import UserModel
from schemas.user import *


class UserRepository:
    def create(self, db: Session, schema: UserCreateSchema) -> UserModel:
        user = UserModel(**schema.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def read(self, db: Session, user_id: int) -> UserModelSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def update(self, db: Session, schema: UserUpdateSchema) -> UserModelSchema:
        user = db.query(UserModel).filter(UserModel.id == schema.id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in schema.dict(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> UserModelSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return user