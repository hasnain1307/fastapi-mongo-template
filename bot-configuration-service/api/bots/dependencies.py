from api.bots.services import BotService
from database import db_object


def get_bot_service() -> BotService:
    """Returns a BotService object"""
    return BotService(db_object=db_object)
