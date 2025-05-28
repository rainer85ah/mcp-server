from dataclasses import dataclass
from data_sources.api_fetcher import HttpFetcher
from data_sources import LocalStorage
from data_sources import WebsiteFetcher
from data_sources import MongoDB
from data_sources import PostgresDB
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
    mongo: MongoDB
    postgres: PostgresDB
    redis: RedisDB
    local_fs: LocalStorage(base_path="/data")
    s3: S3Storage("my-bucket", "us-east-1")
    api: HttpFetcher
    scraper: WebsiteFetcher
