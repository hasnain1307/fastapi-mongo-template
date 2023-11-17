from pydantic import BaseModel, Field
from database import CreateSchemaType


class InTenantSchema(CreateSchemaType):
    name: str = Field(...)


class OutTenantSchema(BaseModel):
    name: str = Field(...)

    class Config:
        from_attributes = True  # If you still want to use it with ORMs


class OutTenantsSchema(OutTenantSchema):
    id: str = Field(...)  # Set default to None and use alias for MongoDB

    class Config:
        from_attributes = True
        populate_by_name = True
