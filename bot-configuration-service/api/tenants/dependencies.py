from api.tenants.services import TenantService
from database import db_object


def get_tenant_service() -> TenantService:
    """Returns a TenantService object"""
    return TenantService(db_object=db_object)
