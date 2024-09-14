from fastapi import Depends
from fastapi.routing import APIRouter

from depends import get_user_service
from schemas.user import UserCreateSchema, UserModelSchema, UserUpdateSchema
from services.user import UserService

router = APIRouter(prefix="/api/user")


@router.post(".create", response_model=UserModelSchema)
def create_user(schema: UserCreateSchema, service: UserService = Depends(get_user_service)):
    return service.create(schema)


@router.get(".get")
def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.read(id)


@router.put(".update")
def update_user(schema: UserUpdateSchema, service: UserService = Depends(get_user_service)):
    return service.update(schema)


@router.delete(".delete")
def delete_user(id: int, service: UserService = Depends(get_user_service)):
    return service.delete(id)