from typing import Optional, Any, List
from asyncpg.pool import Pool
from asyncpg import create_pool, PostgresError, Record
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from apps.mcp.app.core.logger import logger
from apps.mcp.app.resources.base import DataSource



class Postgres(DataSource):
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self.dsn = dsn
        self.pool: Optional[Pool] = None
        self.min_size = min_size
        self.max_size = max_size

    async def connect(self):
        if self.pool is None:
            try:
                self.pool = await create_pool(
                    dsn=self.dsn,
                    min_size=self.min_size,
                    max_size=self.max_size
                )
                logger.info("Postgres pool created")
            except Exception as e:
                logger.exception("Failed to create Postgres pool")
                raise RuntimeError("Database connection failed") from e

    async def close(self):
        if self.pool:
            await self.pool.close()
            logger.info("Postgres pool closed")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(PostgresError),
        reraise=True
    )
    async def read(self, query: str, *args) -> List[Record]:
        await self.connect()
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetch(query, *args)
            except Exception as e:
                logger.exception(f"Postgres read failed: {query} | args={args}")
                raise

    @retry(...)
    async def write(self, query: str, *args) -> str:
        await self.connect()
        async with self.pool.acquire() as conn:
            try:
                return await conn.execute(query, *args)
            except Exception as e:
                logger.exception(f"Postgres write failed: {query} | args={args}")
                raise

    async def fetch_one(self, query: str, *args) -> Optional[Record]:
        """Fetch a single row."""
        await self.connect()
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchrow(query, *args)
            except Exception as e:
                logger.exception(f"Postgres fetch_one failed: {query} | args={args}")
                raise

    async def fetch_value(self, query: str, *args) -> Any:
        """Fetch a single scalar value."""
        row = await self.fetch_one(query, *args)
        return row[0] if row else None

    def record_metric(self, action: str, status: str = "success") -> None:
        logger.info(f"[metric] pg_{action}_{status}")
