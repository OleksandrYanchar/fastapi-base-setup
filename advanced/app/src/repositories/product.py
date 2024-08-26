from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from src.inputs.products import ProductInput, ProductFilter
from src.object_types.products import ProductType
from .base import BaseRepository
from src.configs.db import client, MONGO_DB, MONGO_COLLECTION

class ProductRepository(BaseRepository[ProductType, dict, dict]):
    def __init__(self, client: AsyncIOMotorClient):
        super().__init__(ProductType, client, MONGO_DB, MONGO_COLLECTION)

    async def get_many(self, filters: ProductFilter) -> List[ProductType]:
        query = {}
        if filters.title:
            query['title'] = filters.title
        if filters.min_price is not None:
            query['price'] = {"$gte": filters.min_price}
        if filters.max_price is not None:
            if 'price' in query:
                query['price']['$lte'] = filters.max_price
            else:
                query['price'] = {"$lte": filters.max_price}
        # Add other filters as needed

        cursor = self.collection.find(query)
        results = []
        async for document in cursor:
            results.append(self._model(**document))
        return results

product_repo = ProductRepository(client)
