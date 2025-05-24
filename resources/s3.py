"""
Purpose: Interacts with cloud-based object storage (Amazon S3).
Use case: Read/write/list/delete files in the cloud, often for distributed access or backups.
Example: Upload report.csv to s3://my-data-bucket/reports/.
"""

import aioboto3
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Optional, Any, List
from pathlib import PurePosixPath
from botocore.exceptions import ClientError, BotoCoreError
from apps.mcp.app.resources.base import DataSource


class S3StorageSource(DataSource):
    def __init__(
            self,
            bucket_name: str,
            region_name: Optional[str] = None,
            aws_access_key_id: Optional[str] = None,
            aws_secret_access_key: Optional[str] = None,
            aws_session_token: Optional[str] = None,
            profile_name: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.session_args = {
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token,
            "profile_name": profile_name,
        }

    def _create_session(self):
        return aioboto3.Session(**{k: v for k, v in self.session_args.items() if v is not None})

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, BotoCoreError)),
    )
    async def read(self, key: str, **kwargs) -> bytes:
        key = str(PurePosixPath(key))
        session = self._create_session()
        async with session.client("s3") as s3:
            try:
                response = await s3.get_object(Bucket=self.bucket_name, Key=key)
                async with response["Body"] as stream:
                    return await stream.read()
            except (ClientError, BotoCoreError) as e:
                raise RuntimeError(f"S3 read failed for {key}: {e}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, BotoCoreError)),
    )
    async def write(self, key: str, data: Any, **kwargs) -> None:
        key = str(PurePosixPath(key))
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("S3 write only accepts bytes or bytearray")
        session = self._create_session()
        async with session.client("s3") as s3:
            try:
                await s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)
            except (ClientError, BotoCoreError) as e:
                raise RuntimeError(f"S3 write failed for {key}: {e}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, BotoCoreError)),
    )
    async def list_files(self, prefix: str = "", **kwargs) -> List[str]:
        prefix = str(PurePosixPath(prefix))
        session = self._create_session()
        files = []

        async with session.client("s3") as s3:
            paginator = s3.get_paginator("list_objects_v2")
            try:
                async for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
                    for obj in page.get("Contents", []):
                        files.append(obj["Key"])
                return files
            except (ClientError, BotoCoreError) as e:
                raise RuntimeError(f"S3 list failed for prefix '{prefix}': {e}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, BotoCoreError)),
    )

    async def delete(self, key: str, **kwargs) -> None:
        key = str(PurePosixPath(key))
        session = self._create_session()
        async with session.client("s3") as s3:
            try:
                await s3.delete_object(Bucket=self.bucket_name, Key=key)
            except (ClientError, BotoCoreError) as e:
                raise RuntimeError(f"S3 delete failed for {key}: {e}")
