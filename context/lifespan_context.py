import os
import traceback
from data_sources.mongodb import MongoDB
from data_sources.postgres import PostgresDB
from data_sources.redis import RedisDB
from main import mcp
from utils.logger_config import configure_logger

logger = configure_logger("Lifespan Context")


class LifespanContext:
    def __init__(self):
        self.mongo = MongoDB(
            uri=os.getenv("MONGO_URI", "mongodb://localhost:27017"),
            db_name=os.getenv("MONGO_DB", "testdb"),
            collection_name=os.getenv("MONGO_COLLECTION", "users")
        )
        self.postgres = PostgresDB(
            dsn=os.getenv("POSTGRES_DSN", "postgresql://postgres:password@localhost:5432/testdb"),
            table_name=os.getenv("POSTGRES_TABLE", "users")
        )
        self.redis = RedisDB(
            url=os.getenv("REDIS_URL", "redis://localhost:6379")
        )

    async def startup(self):
        logger.info("🔄 Starting up application resources...")
        try:
            await self.mongo.connect()
            logger.info("✅ MongoDB connected.")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}\n{traceback.format_exc()}")

        try:
            await self.postgres.connect()
            logger.info("✅ PostgreSQL connected.")
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}\n{traceback.format_exc()}")

        try:
            await self.redis.connect()
            logger.info("✅ Redis connected.")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}\n{traceback.format_exc()}")

    async def shutdown(self):
        logger.info("🔁 Shutting down application resources...")
        try:
            await self.mongo.close()
            logger.info("🛑 MongoDB disconnected.")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB disconnection failed: {e}\n{traceback.format_exc()}")

        try:
            await self.postgres.close()
            logger.info("🛑 PostgreSQL disconnected.")
        except Exception as e:
            logger.warning(f"⚠️ PostgreSQL disconnection failed: {e}\n{traceback.format_exc()}")

        try:
            await self.redis.close()
            logger.info("🛑 Redis disconnected.")
        except Exception as e:
            logger.warning(f"⚠️ Redis disconnection failed: {e}\n{traceback.format_exc()}")


lifespan = LifespanContext()

@mcp.on_startup()
async def on_start():
    await lifespan.startup()

@mcp.on_shutdown()
async def on_shutdown():
    await lifespan.shutdown()
