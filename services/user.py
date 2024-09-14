from repositories.user import UserRepository
from schemas.user import *
from services.database import get_db


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, schema: UserCreateSchema) -> UserModelSchema:
        return self._repository.create(next(get_db()), schema)

    def read(self, user_id: int) -> UserModelSchema:
        return self._repository.read(next(get_db()), user_id)

    def update(self, schema: UserUpdateSchema) -> UserModelSchema:
        return self._repository.update(next(get_db()), schema)

    def delete(self, user_id: int) -> UserModelSchema:
        return self._repository.delete(next(get_db()), user_id)