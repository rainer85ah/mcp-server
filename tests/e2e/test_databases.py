import asyncio
from data_sources import MongoDB
from data_sources import PostgresDB
from data_sources.redis import RedisDB


async def test_all():
    # Mongo
    mongo = MongoDB("mongodb://localhost:27017", "testdb", "users")
    await mongo.connect()
    await mongo.write({"name": "Alice", "role": "admin"})
    print("Mongo Read:", await mongo.read({"name": "Alice"}))
    await mongo.delete({"name": "Alice"})
    await mongo.close()

    # Postgres
    postgres = PostgresDB("postgresql://postgres:password@localhost:5432/testdb", "users")
    await postgres.connect()
    await postgres.write({"name": "Bob", "role": "dev"})
    print("Postgres Read:", await postgres.read({"name": "Bob"}))
    await postgres.delete({"name": "Bob"})
    await postgres.close()

    # Redis
    redis = RedisDB("redis://localhost:6379")
    await redis.connect()
    await redis.write({"key": "test", "value": "42"})
    print("Redis Read:", await redis.read({"key": "test"}))
    await redis.delete({"key": "test"})
    await redis.close()

if __name__ == "__main__":
    asyncio.run(test_all())
