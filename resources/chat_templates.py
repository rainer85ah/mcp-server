from fastmcp import Context
from agents.chat import chat_mcp
import aiohttp
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import psycopg2
import logging

logger = logging.getLogger(__name__)

@chat_mcp.resource("resource://website-content/{website_url}")
async def get_website_content(website_url: str, ctx: Context) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(website_url) as response:
                response.raise_for_status()
                return await response.text()
    except Exception as e:
        logger.exception("Website content fetch failed")
        return ""

@chat_mcp.resource("resource://api-data/{api_url}")
async def get_api_data(api_url: str, ctx: Context) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.exception("API data fetch failed")
        return {}

@chat_mcp.resource("resource://github-repo/{repository_url}")
async def get_github_repo(repository_url: str, ctx: Context) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(repository_url) as response:
                response.raise_for_status()
                return await response.text()
    except Exception as e:
        logger.exception("GitHub repo fetch failed")
        return ""

@chat_mcp.resource("resource://mongo-data/{collection_name}")
async def get_mongo_data(collection_name: str, ctx: Context) -> dict:
    try:
        mongo = ctx.fastmcp.app.state.lifespan.mongo
        db = mongo.get_default_database()
        document = db[collection_name].find_one()
        return document or {}
    except Exception as e:
        logger.exception("MongoDB fetch failed")
        return {}

@chat_mcp.resource("resource://postgres-data/{postgres_dsn}")
async def get_postgres_data(postgres_dsn: str, ctx: Context) -> dict:
    try:
        with psycopg2.connect(postgres_dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT key, value FROM your_table LIMIT 1;")
                result = cursor.fetchone()
                if result:
                    return {"key": result[0], "value": result[1]}
    except Exception as e:
        logger.exception("PostgreSQL fetch failed")
    return {}

@chat_mcp.resource("resource://s3-data/{s3_bucket_name}/{s3_bucket_key}")
async def get_s3_data(s3_bucket_name: str, s3_bucket_key: str, ctx: Context) -> str:
    try:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=s3_bucket_name, Key=s3_bucket_key)
        return response["Body"].read().decode("utf-8")
    except (BotoCoreError, ClientError) as e:
        logger.exception("S3 data fetch failed")
        return ""

@chat_mcp.resource("resource://local-file/{file_path}")
async def get_local_file(file_path: str, ctx: Context) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.exception("Local file read failed")
        return ""
