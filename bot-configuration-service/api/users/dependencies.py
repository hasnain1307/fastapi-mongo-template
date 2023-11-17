from api.users.services import UserService
from database import bot_config_db


def get_user_service() -> UserService:
    """Returns a UserService object"""
    return UserService(bot_config_db=bot_config_db)
