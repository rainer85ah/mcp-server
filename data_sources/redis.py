import redis.asyncio as redis
from typing import Any, Dict, List
from data_sources.abstract_db import BaseDB
from utils.logger_config import configure_logger
from utils.retries import db_retry


logger = configure_logger("RedisDB")


class RedisDB(BaseDB):
    def __init__(self, url: str):
        self.url = url
        self.client = None

    async def connect(self):
        if self.client is None:
            self.client = redis.from_url(self.url)
            logger.info(f"Connected to Redis: {self.url}")

    async def close(self):
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")

    db_retry()
    async def read(self, filter_query: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        await self.connect()
        key = filter_query.get("key")
        value = await self.client.get(key)
        return [{"key": key, "value": value.decode() if value else None}]

    db_retry()
    async def write(self, document: Dict[str, Any], **kwargs) -> None:
        await self.connect()
        await self.client.set(document["key"], document["value"])

    db_retry()
    async def update(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False) -> int:
        await self.connect()
        await self.client.set(filter_query["key"], update_doc["value"])
        return 1

    db_retry()
    async def delete(self, filter_query: Dict[str, Any]) -> int:
        await self.connect()
        return await self.client.delete(filter_query["key"])
