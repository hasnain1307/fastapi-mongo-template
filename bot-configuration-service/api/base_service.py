from typing import Generic, Optional, TypeVar, Type
from bson import ObjectId

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import BaseMongoModel
from api.exceptions import ObjectNotFoundException, UniqueKeyViolationException

ModelType = TypeVar("ModelType", bound=BaseMongoModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], collection_name: str, db_object: AsyncIOMotorDatabase):
        self.model = model
        self.db = db_object
        self.collection = db_object[collection_name]

    async def get(self, id: str) -> Optional[ModelType]:
        obj = await self.collection.find_one({"_id": ObjectId(id), "is_deleted": False})
        if obj is None:
            raise ObjectNotFoundException(status_code=404, detail="Not Found")
        return self.model.from_mongo(obj)

    async def list(self) -> list[ModelType]:
        objs = []
        cursor = self.collection.find({"is_deleted": False})
        async for obj in cursor:
            objs.append(self.model.from_mongo(obj))  # Convert each MongoDB document
        return objs

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            result = await self.collection.insert_one(obj_in.dict())
            return await self.get(result.inserted_id)
        except UniqueKeyViolationException as e:  # You might need a custom exception for MongoDB
            raise UniqueKeyViolationException(status_code=409, detail="Conflict Error")

    async def update(self, id: str, obj: UpdateSchemaType) -> Optional[ModelType]:
        await self.collection.update_one({"_id": id}, {"$set": obj.dict(exclude_unset=True)})
        return await self.get(id)

    async def delete(self, id: str) -> None:
        collection_names = await self.db.list_collection_names()

        # Iterate over each collection and set is_deleted to True for documents with the given id
        for collection_name in collection_names:
            collection = self.db[collection_name]
            await collection.update_many({"reference_id": ObjectId(id)}, {"$set": {"is_deleted": True}})

        # Additionally, update the specific collection of this BaseService instance
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_deleted": True}})
