from typing import Optional

from api.base_service import BaseService


class UserService(BaseService):
    def __init__(self, db_object):
        super().__init__(collection_name="users", db_object=db_object)

    async def user_exists(self, username: Optional[str] = None, email: Optional[str] = None) -> bool | ValueError:
        """Check if user exists"""
        if username:
            user = await self.collection.find_one({"name": username, "is_deleted": False})
        elif email:
            user = await self.collection.find_one({"email": email, "is_deleted": False})
        else:
            raise ValueError("You must provide either username or email")
        return True if user else False
