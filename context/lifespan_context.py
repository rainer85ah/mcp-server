from main import mcp
from data_sources import MongoDB
from data_sources import PostgresDB
from data_sources.redis import RedisDB
from utils.logger_config import configure_logger


logger = configure_logger("Lifespan Context")


class LifespanContext:
    def __init__(self):
        self.mongo = MongoDB(
            uri="mongodb://localhost:27017",
            db_name="testdb",
            collection_name="users"
        )
        self.postgres = PostgresDB(
            dsn="postgresql://postgres:password@localhost:5432/testdb",
            table_name="users"
        )
        self.redis = RedisDB(
            url="redis://localhost:6379"
        )

    async def startup(self):
        logger.info("Initializing database connections...")
        await self.mongo.connect()
        await self.postgres.connect()
        await self.redis.connect()
        logger.info("All databases connected.")

    async def shutdown(self):
        logger.info("Closing database connections...")
        await self.mongo.close()
        await self.postgres.close()
        await self.redis.close()
        logger.info("All databases closed.")


if __name__ == '__main__':
    # usage example
    lifespan = LifespanContext()

    @mcp.on_startup()
    async def on_start():
        await lifespan.startup()

    @mcp.on_shutdown()
    async def on_shutdown():
        await lifespan.shutdown()
