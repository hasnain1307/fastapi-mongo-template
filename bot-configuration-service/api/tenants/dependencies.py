from api.tenants.services import TenantService
from database import bot_config_db


def get_tenant_service() -> TenantService:
    """Returns a TenantService object"""
    return TenantService(bot_config_db=bot_config_db)
