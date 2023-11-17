from typing import Optional
# from api.tenants.schemas import InTenantSchema
from api.base_service import BaseService
from database import TenantModel


class TenantService(BaseService):
    def __init__(self, bot_config_db):
        super().__init__(collection_name="tenants", model=TenantModel, db_object=bot_config_db)

    async def tenant_exists(self, name: Optional[str] = None) -> bool:
        """Check if tenant exists"""
        if name:
            tenant = await self.collection.find_one({"name": name, "is_deleted": False})
            return bool(tenant)
        else:
            raise ValueError("You must provide a tenant name")
