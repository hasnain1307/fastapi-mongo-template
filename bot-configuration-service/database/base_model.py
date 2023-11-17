from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BaseMongoModel(BaseModel):
    @classmethod
    def from_mongo(cls, data: dict):
        if "_id" in data:
            data["id"] = str(data.pop("_id"))
        return cls(**data)


class CreateSchemaType(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    is_deleted: bool = Field(default=False)
    deleted_on: Optional[datetime] = Field(default=None)
