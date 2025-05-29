from dataclasses import dataclass
from os import environ
from typing import Optional
from data_sources.api_fetcher import HttpFetcher
from data_sources.filesystem import LocalStorage
from data_sources.http_fetcher import WebsiteFetcher
from data_sources.mongodb import MongoDB
from data_sources.postgres import PostgresDB
from data_sources.redis import RedisDB
from data_sources.s3 import S3Storage
from utils.logger_config import configure_logger


logger = configure_logger("AppContext")


@dataclass
class AppContext:
    mongo: Optional[MongoDB] = None
    postgres: Optional[PostgresDB] = None
    redis: Optional[RedisDB] = None
    local_fs: Optional[LocalStorage] = None
    s3: Optional[S3Storage] = None
    api: Optional[HttpFetcher] = None
    scraper: Optional[WebsiteFetcher] = None

    def startup(self):
        if self.mongo:
            self.mongo.connect()
        if self.postgres:
            self.postgres.connect()
        if self.redis:
            self.redis.connect()
        # Add any other startup hooks here

    def shutdown(self):
        if self.mongo:
            self.mongo.close()
        if self.postgres:
            self.postgres.close()
        if self.redis:
            self.redis.close()
        # Add any other shutdown hooks here


def create_app_context() -> AppContext:
    return AppContext(
        api=HttpFetcher(),
        scraper=WebsiteFetcher(),
        local_fs=LocalStorage(base_path=environ.get("LOCAL_BASE_PATH", "/data")),
        s3=S3Storage(
            bucket_name=environ.get("S3_BUCKET", "my-bucket"),
            region=environ.get("S3_REGION", "us-east-1")
        ),
        redis=RedisDB(
            url=environ.get("REDIS_URL", "redis://localhost:6379/0")
        ),
        postgres=PostgresDB(
            dsn=environ.get("POSTGRES_DSN", "postgresql://user:pass@host:5432/db"),
            table_name=environ.get("POSTGRES_TABLE", "users")
        ),
        mongo=MongoDB(
            uri=environ.get("MONGO_URI", "mongodb://user:pass@host:27017/db"),
            db_name=environ.get("MONGO_DB", "mongo-prod"),
            collection_name=environ.get("MONGO_COLLECTION", "users")
        ),
    )
