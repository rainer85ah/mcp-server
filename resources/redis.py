import json
from typing import Any, Optional, Union, Dict, List
from aioredis import from_url, Redis, RedisError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from apps.mcp.app.core.logger import logger
from apps.mcp.app.resources.base import DataSource


class RedisSource(DataSource):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[Redis] = None

    async def connect(self) -> Redis:
        if self.redis is None or self.redis.closed:
            self.redis = await from_url(self.redis_url, decode_responses=False)
        return self.redis

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((RedisError, ConnectionError)),
    )
    async def read(self, key: str, json_decode: bool = False, **kwargs) -> Optional[Any]:
        redis = await self.connect()
        try:
            value = await redis.get(key)
            if value is not None:
                return json.loads(value) if json_decode else value
            return None
        except RedisError as e:
            logger.exception(f"Redis read failed for key={key}")
            raise RuntimeError(f"Redis read failed for key '{key}': {e}")

    @retry(...)
    async def write(
            self,
            key: str,
            data: Union[bytes, str, dict, list],
            ttl: Optional[int] = None,
            json_encode: bool = False,
            **kwargs
    ) -> None:
        redis = await self.connect()
        try:
            payload = json.dumps(data).encode() if json_encode else (
                data.encode() if isinstance(data, str) else data
            )
            await redis.set(key, payload, ex=ttl)
        except RedisError as e:
            logger.exception(f"Redis write failed for key={key}")
            raise RuntimeError(f"Redis write failed for key '{key}': {e}")

    async def delete(self, key: str, **kwargs) -> None:
        redis = await self.connect()
        try:
            await redis.delete(key)
        except RedisError as e:
            logger.exception(f"Redis delete failed for key={key}")
            raise RuntimeError(f"Redis delete failed for key '{key}': {e}")

    # --- Hash Methods ---
    async def hset(self, key: str, field: str, value: Union[str, bytes], **kwargs) -> None:
        redis = await self.connect()
        if isinstance(value, str):
            value = value.encode()
        await redis.hset(key, field, value)

    async def hget(self, key: str, field: str, **kwargs) -> Optional[bytes]:
        redis = await self.connect()
        return await redis.hget(key, field)

    async def hgetall(self, key: str, **kwargs) -> Dict[str, bytes]:
        redis = await self.connect()
        raw = await redis.hgetall(key)
        return {k.decode(): v for k, v in raw.items()}

    # --- Set Methods ---
    async def sadd(self, key: str, *values: Union[str, bytes], **kwargs) -> int:
        redis = await self.connect()
        encoded = [v.encode() if isinstance(v, str) else v for v in values]
        return await redis.sadd(key, *encoded)

    async def smembers(self, key: str, **kwargs) -> List[bytes]:
        redis = await self.connect()
        return list(await redis.smembers(key))

    # --- List Methods ---
    async def lpush(self, key: str, *values: Union[str, bytes], **kwargs) -> int:
        redis = await self.connect()
        encoded = [v.encode() if isinstance(v, str) else v for v in values]
        return await redis.lpush(key, *encoded)

    async def lrange(self, key: str, start: int = 0, end: int = -1, **kwargs) -> List[bytes]:
        redis = await self.connect()
        return await redis.lrange(key, start, end)

    async def close(self) -> None:
        if self.redis and not self.redis.closed:
            await self.redis.close()

    # --- Optional: metrics hooks (you can integrate with Prometheus client here) ---
    def record_metric(self, action: str, status: str = "success") -> None:
        logger.info(f"[metric] redis_{action}_{status}")
