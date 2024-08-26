from typing import Generic, Optional, TypeVar, List, Type
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], client: AsyncIOMotorClient, database: str, collection: str) -> None:
        self._model = model
        self.client = client
        self.db = self.client[database]
        self.collection = self.db[collection]

    async def find_by_id(self, id: str) -> Optional[ModelType]:
        print(f"Finding by id: {id}")
        obj = await self.collection.find_one({"_id": ObjectId(id)})
        print(f"Found object: {obj}")
        if obj:
            obj["id"] = str(obj["_id"])
            return self._model(**obj)
        return None

    async def get(self, **kwargs) -> Optional[ModelType]:
        print(f"Getting with kwargs: {kwargs}")
        document = await self.collection.find_one(kwargs)
        print(f"Found document: {document}")
        if document:
            document["id"] = str(document["_id"])
            return self._model(**document)
        return None

    async def get_many(self, filters: dict) -> List[ModelType]:
        print(f"Getting many with filters: {filters}")
        cursor = self.collection.find(filters)
        results = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            results.append(self._model(**document))
        print(f"Found documents: {results}")
        return results

    async def create(self, obj_in: dict) -> ModelType:
        print(f"Creating object: {obj_in}")
        result = await self.collection.insert_one(obj_in)
        new_document = await self.collection.find_one({"_id": result.inserted_id})
        print(f"Created document: {new_document}")
        new_document["id"] = str(new_document["_id"])
        return self._model(**new_document)

    async def delete(self, id: str) -> bool:
        print(f"Deleting by id: {id}")
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        print(f"Delete result: {result.deleted_count}")
        return result.deleted_count == 1

    async def update(self, id: str, update_data: dict) -> Optional[ModelType]:
        print(f"Updating id: {id} with data: {update_data}")
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        print(f"Update result: {result.modified_count}")
        if result.modified_count == 1:
            updated_document = await self.collection.find_one({"_id": ObjectId(id)})
            print(f"Updated document: {updated_document}")
            if updated_document:
                updated_document["id"] = str(updated_document["_id"])
                return self._model(**updated_document)
        return None
