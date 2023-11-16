from api.users.services import UserService
from database import db_object


def get_user_service() -> UserService:
    """Returns a UserService object"""
    return UserService(db_object=db_object)
