from typing import Optional
from .base_model import BaseMongoModel


class TenantModel(BaseMongoModel):
    id: Optional[str] = None  # Optional ID field, will be populated from MongoDB's _id
    name: str  # Example field, you can add more fields as per your requirements
    is_deleted: bool = False  # Default to False, can be set to True for soft delete
