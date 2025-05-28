from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from botocore.exceptions import ClientError, BotoCoreError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import redis.exceptions
import pymongo.errors
import psycopg2
import asyncpg


def db_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((
            redis.exceptions.RedisError,
            pymongo.errors.PyMongoError,
            psycopg2.DatabaseError,
            asyncpg.PostgresError,
            ConnectionError,
            TimeoutError,
        )),
    )


def s3_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, BotoCoreError)),
    )

def local_fs_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((OSError, PermissionError, FileNotFoundError)),
    )


def http_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((Exception,))
    )

