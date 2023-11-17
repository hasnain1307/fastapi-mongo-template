from typing import Optional

from api.base_service import BaseService


class BotService(BaseService):
    def __init__(self, bot_config_db):
        super().__init__(collection_name="bots", db_object=bot_config_db)

    async def bot_exists(self, name: Optional[str] = None) -> bool:
        """Check if tenant exists"""
        if name:
            bot = await self.collection.find_one({"name": name, "is_deleted": False})
            return bool(bot)
        else:
            raise ValueError("You must provide a bot name")
