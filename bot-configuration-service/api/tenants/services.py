from typing import Optional

from api.base_service import BaseService


class TenantService(BaseService):
    def __init__(self, db_object):
        super().__init__(collection_name="tenants", db=db_object)

    async def tenant_exists(self, name: Optional[str] = None) -> bool:
        """Check if tenant exists"""
        if name:
            tenant = await self.collection.find_one({"name": name, "is_deleted": False})
            return bool(tenant)
        else:
            raise ValueError("You must provide a tenant name")
