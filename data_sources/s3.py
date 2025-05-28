"""
Purpose: Interacts with cloud-based object storage (Amazon S3).
Use case: Read/write/list/delete files in the cloud, often for distributed access or backups.
Example: Upload report.csv to s3://my-data-bucket/reports/.
"""
import aiofiles.tempfile
import boto3
from botocore.exceptions import ClientError
from data_sources.abstract_storage import BaseStorage
from utils.logger_config import configure_logger
from utils.retries import s3_retry


logger = configure_logger("S3Storage")


class S3Storage(BaseStorage):
    def __init__(self, bucket: str, region: str):
        self.bucket = bucket
        self.s3 = boto3.client("s3", region_name=region)

    @s3_retry()
    async def upload(self, path: str, data: bytes):
        try:
            with aiofiles.tempfile.NamedTemporaryFile(delete=False) as tmp:
                await tmp.write(data)
                tmp.flush()
                self.s3.upload_file(tmp.name, self.bucket, path)
            logger.info(f"Uploaded to S3: {path}")
        except ClientError as e:
            logger.error("S3 upload failed", exc_info=e)
            raise

    @s3_retry()
    async def download(self, path: str) -> bytes:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=path)
            return obj["Body"].read()
        except ClientError as e:
            logger.error("S3 download failed", exc_info=e)
            raise

    @s3_retry()
    async def delete(self, path: str) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=path)
            logger.info(f"Deleted from S3: {path}")
        except ClientError as e:
            logger.error("S3 delete failed", exc_info=e)
            raise
