from repositories.user import UserRepository
from services.user import UserService

# repositories
user_repository = UserRepository()

# services
user_service = UserService(user_repository)


# getters
def get_user_service() -> UserService:
    return user_service