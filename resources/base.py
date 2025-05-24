import abc
from typing import Any


class DataSource(abc.ABC):

    @abc.abstractmethod
    async def read(self, key: str, **kwargs) -> Any:
        raise NotImplementedError("Read operation not implemented")

    async def write(self, key: str, data: Any, **kwargs) -> None:
        raise NotImplementedError("Write operation not implemented")


"""
async def example_usage():
    # Local file read
    local = LocalFileSource()
    data = await local.read('example.pdf')  # binary data, parse separately

    # S3 read/write
    s3 = S3StorageSource('my-bucket')
    s3_data = await s3.read('file.txt')
    await s3.write('upload.txt', b'Hello world')

    # Redis
    redis = RedisSource("redis://localhost")
    await redis.write("key1", b"value1")
    val = await redis.read("key1")

    # PostgreSQL
    pg = PostgresSource(dsn="postgresql://user:password@host/dbname")
    rows = await pg.read("SELECT * FROM stocks WHERE symbol=$1", "AAPL")

    # MongoDB
    mongo = MongoSource("mongodb://localhost:27017", "mydb", "mycollection")
    docs = await mongo.read({"symbol": "AAPL"})

    # REST API
    api = RestApiSource("https://api.example.com", headers={"Authorization": "Bearer token"})
    info = await api.read("stocks/AAPL")

asyncio.run(example_usage())
"""
