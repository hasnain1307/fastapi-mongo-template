from fastapi import APIRouter, Depends, status
from logger import logger
from api.constants import ErrorCodes
from api.exceptions import ObjectNotFoundException, UniqueKeyViolationException
from api.schemas import ResourceCreatedResponse, ResourceDeletedResponse
from api.tenants.dependencies import get_tenant_service
from api.tenants.schemas import InTenantSchema, OutTenantSchema, OutTenantsSchema
from api.tenants.services import TenantService

router = APIRouter()


@router.get("/", tags=["Get all tenants"], response_model=list[OutTenantsSchema], status_code=status.HTTP_200_OK)
async def get_all_tenants(tenant_service: TenantService = Depends(get_tenant_service)) -> list[OutTenantsSchema]:
    """Returns all tenants"""
    logger.debug("Get all tenants endpoint hit")
    tenants = await tenant_service.list()
    return tenants


@router.get("/{id}", tags=["Get tenant by id"], response_model=OutTenantSchema, status_code=status.HTTP_200_OK)
async def get_tenant_by_id(id: str, tenant_service: TenantService = Depends(get_tenant_service)) -> OutTenantSchema:
    """Return single tenant by id"""
    logger.info(f"Fetching tenant with id {id}")
    try:
        tenant = await tenant_service.get(id=id)
    except ObjectNotFoundException as e:
        logger.debug(f"Tenant with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.TENANT_NOT_FOUND
        raise e
    return tenant


@router.post("/", tags=["Create tenant"], response_model=ResourceCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant: InTenantSchema, tenant_service: TenantService = Depends(get_tenant_service)):
    """Create tenant. If tenant already exists, return 409 Conflict error"""
    if await tenant_service.tenant_exists(name=tenant.name):
        logger.debug(f"Tenant with this name {tenant.name} already exists. Throwing 409 Conflict error")
        raise UniqueKeyViolationException(status_code=status.HTTP_409_CONFLICT, detail=ErrorCodes.TENANT_ALREADY_EXISTS)

    new_tenant = await tenant_service.create(tenant)
    logger.info(f"Tenant created with id: {new_tenant.id}")
    return ResourceCreatedResponse(detail="Tenant created successfully", id=new_tenant.id)


@router.put("/{id}", tags=["Update tenant"], response_model=OutTenantSchema, status_code=status.HTTP_200_OK)
async def update_tenant(id: str, tenant: InTenantSchema, tenant_service: TenantService = Depends(get_tenant_service)):
    """Update tenant by id. Also soft delete tenant if is_deleted is True"""
    try:
        await tenant_service.update(id=id, obj=tenant)
        updated_tenant = await tenant_service.get(id=id)
    except UniqueKeyViolationException as e:
        logger.debug(f"Tenant with this name {tenant.name} already exists. Throwing 409 Conflict error")
        e.detail = ErrorCodes.TENANT_ALREADY_EXISTS
        raise e
    except ObjectNotFoundException as e:
        logger.debug(f"Tenant with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.TENANT_NOT_FOUND
        raise e
    logger.info(f"Tenant with id {id} updated")
    return updated_tenant


@router.delete("/{id}", tags=["Delete Tenant"], response_model=ResourceDeletedResponse, status_code=status.HTTP_200_OK)
async def delete_tenant(id: str,
                        tenant_service: TenantService = Depends(get_tenant_service)) -> ResourceDeletedResponse:
    """Soft delete tenant by id"""
    await tenant_service.delete(id=id)
    logger.info(f"Tenant with {id} deleted")
    return ResourceDeletedResponse(detail="Tenant deleted successfully", id=id)
