import asyncpg
from typing import List, Dict, Any
from data_sources.abstract_db import BaseDB
from utils.logger_config import configure_logger
from utils.retries import db_retry


logger = configure_logger("PostgresDB")


class PostgresDB(BaseDB):
    def __init__(self, dsn: str, table_name: str):
        self.dsn = dsn
        self.table = table_name
        self.pool = None

    async def connect(self):
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(dsn=self.dsn)
                logger.info(f"Connected to Postgres: {self.dsn}")
            except Exception as e:
                logger.exception("Postgres connection failed")
                raise RuntimeError("Postgres connection failed") from e

    async def close(self):
        if self.pool:
            await self.pool.close()
            logger.info("Postgres connection closed")

    @db_retry()
    async def read(self, filter_query: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        await self.connect()
        where_clause = " AND ".join(f"{k} = ${i+1}" for i, k in enumerate(filter_query))
        values = list(filter_query.values())
        sql = f"SELECT * FROM {self.table} WHERE {where_clause}"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values)
            return [dict(row) for row in rows]

    @db_retry()
    async def write(self, document: Dict[str, Any], **kwargs) -> None:
        await self.connect()
        keys = ", ".join(document.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(document)))
        values = list(document.values())
        sql = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, *values)

    @db_retry()
    async def update(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False) -> int:
        # Postgres upsert (INSERT ... ON CONFLICT) logic can be added here
        raise NotImplementedError("Update logic depends on table schema")

    @db_retry()
    async def delete(self, filter_query: Dict[str, Any]) -> int:
        await self.connect()
        where_clause = " AND ".join(f"{k} = ${i+1}" for i, k in enumerate(filter_query))
        values = list(filter_query.values())
        sql = f"DELETE FROM {self.table} WHERE {where_clause}"
        async with self.pool.acquire() as conn:
            result = await conn.execute(sql, *values)
            return int(result.split()[-1])  # e.g., "DELETE 3"
