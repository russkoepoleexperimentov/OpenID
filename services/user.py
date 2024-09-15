import hashlib

from repositories.user import UserRepository
from schemas.user import *
from services.database import get_db


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, schema: UserCreateSchema) -> UserOutSchema:
        schema.password = self.encrypt_password(schema.password)
        return self._repository.create(next(get_db()), schema)

    def read(self, user_id: int) -> UserOutSchema:
        return self._repository.read(next(get_db()), user_id)

    def update(self, schema: UserUpdateSchema) -> UserOutSchema:
        return self._repository.update(next(get_db()), schema)

    def delete(self, user_id: int) -> UserOutSchema:
        return self._repository.delete(next(get_db()), user_id)

    def encrypt_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def authenticate(self, schema: UserAuthenticateSchema) -> UserOutSchema:
        encrypted_password = self.encrypt_password(schema.password)
        return self._repository.authenticate(next(get_db()), schema.username, encrypted_password)