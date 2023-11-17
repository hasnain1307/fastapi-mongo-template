from pydantic import BaseModel


class ResourceCreatedResponse(BaseModel):
    detail: str
    id: str


class ResourceDeletedResponse(BaseModel):
    detail: str


class ConflictDetail(BaseModel):
    detail: str
