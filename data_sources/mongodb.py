from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from data_sources.abstract_db import BaseDB
from utils.logger_config import configure_logger
from utils.retries import db_retry


logger = configure_logger("MongoDB")


class MongoDB(BaseDB):
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.collection = None

    async def connect(self):
        if self.client is None:
            try:
                self.client = AsyncIOMotorClient(self.uri)
                await self.client.server_info()
                self.collection = self.client[self.db_name][self.collection_name]
                logger.info(f"Connected to MongoDB: {self.db_name}.{self.collection_name}")
            except PyMongoError as e:
                logger.exception("MongoDB connection failed")
                raise RuntimeError("MongoDB connection failed") from e

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    db_retry()
    async def read(self, filter_query: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        await self.connect()
        cursor = self.collection.find(filter_query, **kwargs)
        return [doc async for doc in cursor]

    db_retry()
    async def write(self, document: Dict[str, Any], **kwargs) -> None:
        await self.connect()
        await self.collection.insert_one(document, **kwargs)

    db_retry()
    async def update(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False) -> int:
        await self.connect()
        result = await self.collection.update_many(filter_query, {"$set": update_doc}, upsert=upsert)
        return result.modified_count

    db_retry()
    async def delete(self, filter_query: Dict[str, Any]) -> int:
        await self.connect()
        result = await self.collection.delete_many(filter_query)
        return result.deleted_count
