from os import makedirs
from aiofiles import os, open
from pathlib import Path
from data_sources.abstract_storage import BaseStorage
from utils.logger_config import configure_logger
from utils.retries import local_fs_retry


logger = configure_logger("LocalStorage")


class LocalStorage(BaseStorage):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        if not self.base_path.is_dir():
            raise ValueError(f"Base path '{self.base_path}' is not a valid directory")

    @local_fs_retry()
    async def upload(self, path: str, data: bytes):
        full_path = (self.base_path / path).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        makedirs(full_path.parent, exist_ok=True)
        async with open(full_path, 'wb') as f:
            await f.write(data)
        logger.info(f"Uploaded to {full_path}")

    @local_fs_retry()
    async def download(self, path: str) -> bytes:
        full_path = (self.base_path / path).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        async with open(full_path, 'rb') as f:
            return await f.read()

    @local_fs_retry()
    async def delete(self, path: str) -> None:
        full_path = (self.base_path / path).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        await os.remove(full_path)
        logger.info(f"Deleted {full_path}")

