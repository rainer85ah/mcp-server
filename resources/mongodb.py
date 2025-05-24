from typing import Optional, List, Dict, Any, Union
from motor import motor_asyncio
from motor.core import AgnosticCollection
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from apps.mcp.app.core.logger import logger
from apps.mcp.app.resources.base import DataSource


class MongoDB(DataSource):
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client: Optional[motor_asyncio.AsyncIOMotorClient] = None
        self.collection: Optional[AgnosticCollection] = None

    async def connect(self):
        if self.client is None:
            try:
                self.client = motor_asyncio.AsyncIOMotorClient(self.uri)
                # Optional: trigger server_info to verify connection
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(PyMongoError),
        reraise=True
    )
    async def read(self, filter_query: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        await self.connect()
        cursor = self.collection.find(filter_query, **kwargs)
        results = []
        try:
            async for doc in cursor:
                results.append(doc)
            return results
        except PyMongoError as e:
            logger.exception(f"Mongo read failed: filter={filter_query}")
            raise

    @retry(...)
    async def write(self, document: Dict[str, Any], **kwargs) -> None:
        await self.connect()
        try:
            await self.collection.insert_one(document, **kwargs)
        except PyMongoError as e:
            logger.exception(f"Mongo write failed: document={document}")
            raise

    @retry(...)
    async def update(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False) -> int:
        await self.connect()
        try:
            result = await self.collection.update_many(filter_query, update_doc, upsert=upsert)
            return result.modified_count
        except PyMongoError as e:
            logger.exception(f"Mongo update failed: filter={filter_query}, update={update_doc}")
            raise

    @retry(...)
    async def delete(self, filter_query: Dict[str, Any]) -> int:
        await self.connect()
        try:
            result = await self.collection.delete_many(filter_query)
            return result.deleted_count
        except PyMongoError as e:
            logger.exception(f"Mongo delete failed: filter={filter_query}")
            raise
