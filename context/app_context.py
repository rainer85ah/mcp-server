from dataclasses import dataclass
from data_sources.api_fetcher import HttpFetcher
from data_sources.filesystem import LocalStorage
from data_sources.http_fetcher import WebsiteFetcher
from data_sources.mongodb import MongoDB
from data_sources.postgres import PostgresDB
from data_sources.redis import RedisDB
from data_sources.s3 import S3Storage


@dataclass
class AppContext:
    mongo: MongoDB
    postgres: PostgresDB
    redis: RedisDB
    local_fs: LocalStorage
    s3: S3Storage
    api: HttpFetcher
    scraper: WebsiteFetcher


class MainMCPContext:
    api: HttpFetcher()
    scraper: WebsiteFetcher()
    local_fs: LocalStorage(base_path="/data")
    s3: S3Storage("my-bucket", "us-east-1")
    redis: RedisDB(url="postgresql://username:password@host:port/database_index")
    postgres: PostgresDB(dsn="postgresql://username:password@host:port/db_name", table_name="users")
    mongo: MongoDB(uri="mongodb://username:password@host:port/db_name", db_name="mongo-prod", collection_name="users")

