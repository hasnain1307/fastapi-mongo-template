from pydantic import BaseModel, Field, validator
from typing import List
from enum import Enum


class Stages(str, Enum):
    NEW = "new"
    ADDED = "bot added"
    TRAINED = "trained"
    SIMULATED = "simulated"
    CHANNELS = "channels added"
    DEPLOYED = "deployed"


class InBotSchema(BaseModel):
    name: str = Field(...)
    industry: str = Field(...)
    image: str = Field(None)
    channels: List[str] = Field(...)
    languages: List[str] = Field(...)
    tenant_id: int = Field(...)
    stage: Stages = Field(default_factory=lambda: Stages.NEW)


# class InBotUpdateSchema(InBotSchema):
#     is_deleted: bool = Field(False)
class OutBotSchema(BaseModel):
    name: str = Field(...)
    image: str = Field(None)

    class Config:
        from_attributes = True


class OutBotsSchema(OutBotSchema):
    id: str = Field(...)

    class Config:
        from_attributes = True
