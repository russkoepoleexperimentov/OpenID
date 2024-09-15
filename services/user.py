import hashlib

import jwt
from fastapi import HTTPException

from configs.jwt import JWT_SECRET, JWT_ALGORITHM, JWT_PAYLOAD_USERNAME, JWT_PAYLOAD_PASSWORD
from repositories.user import UserRepository
from schemas.user import *
from services.database import get_db


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, schema: UserCreateSchema) -> UserOutSchema:
        schema.password = self.encrypt_password(schema.password)
        access_token = self.encode_auth_data(schema.username, schema.password)
        return self._repository.create(next(get_db()), schema, access_token)

    def read(self, user_id: int) -> UserOutSchema:
        return self._repository.read(next(get_db()), user_id)

    def update(self, schema: UserUpdateSchema) -> UserOutSchema:
        user = self._repository.get_by_access_token(next(get_db()), schema.access_token)
        return self._repository.update(next(get_db()), schema, user.id)

    def delete(self, schema: UserDeleteSchema) -> UserOutSchema:
        user = self._repository.get_by_access_token(next(get_db()), schema.access_token)

        # additional safety check: validate actual password
        user_data = self.decode_auth_data(schema.access_token)
        encrypted_password = self.encrypt_password(schema.password)

        if user_data[JWT_PAYLOAD_PASSWORD] != encrypted_password:
            raise HTTPException(status_code=403, detail='Incorrect password')

        return self._repository.delete(next(get_db()), user.id)

    def encrypt_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def encode_auth_data(self, username: str, password: str) -> str:
        payload = {
            JWT_PAYLOAD_USERNAME: username,
            JWT_PAYLOAD_PASSWORD: password,
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def decode_auth_data(self, access_token) -> dict[str, str]:
        return jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    def authenticate(self, schema: UserAuthenticateSchema) -> UserTokenSchema:
        encrypted_password = self.encrypt_password(schema.password)
        return self._repository.authenticate(next(get_db()), schema.username, encrypted_password)