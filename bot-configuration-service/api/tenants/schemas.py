from pydantic import BaseModel, Field


class InTenantSchema(BaseModel):
    name: str = Field(...)


class OutTenantSchema(BaseModel):
    name: str = Field(...)

    class Config:
        orm_mode = True  # If you still want to use it with ORMs


class OutTenantsSchema(OutTenantSchema):
    id: str = Field(...)  # Changed from int to str for MongoDB ObjectID

    class Config:
        orm_mode = True
