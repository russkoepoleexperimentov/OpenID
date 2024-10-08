from fastapi import Depends
from fastapi.routing import APIRouter

from depends import get_user_service
from schemas.user import UserCreateSchema, UserOutSchema, UserUpdateSchema, UserAuthenticateSchema, UserTokenSchema, \
    UserDeleteSchema
from services.user import UserService

router = APIRouter(prefix="/api/user")


@router.post(".create", response_model=UserOutSchema)
def create_user(schema: UserCreateSchema, service: UserService = Depends(get_user_service)):
    return service.create(schema)


@router.get(".get", response_model=UserOutSchema)
def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.read(id)


@router.put(".update", response_model=UserOutSchema)
def update_user(schema: UserUpdateSchema, service: UserService = Depends(get_user_service)):
    return service.update(schema)


@router.delete(".delete", response_model=UserOutSchema)
def delete_user(schema: UserDeleteSchema, service: UserService = Depends(get_user_service)):
    return service.delete(schema)


@router.post(".authenticate", response_model=UserTokenSchema)
def authenticate(schema: UserAuthenticateSchema, service: UserService = Depends(get_user_service)):
    return service.authenticate(schema)