from api.bots.services import BotService
from database import bot_config_db


def get_bot_service() -> BotService:
    """Returns a BotService object"""
    return BotService(bot_config_db=bot_config_db)
