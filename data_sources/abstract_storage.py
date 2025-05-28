from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorage(ABC):
    @abstractmethod
    async def upload(self, path: str, data: bytes | BinaryIO):
        pass

    @abstractmethod
    async def download(self, path: str) -> bytes:
        pass

    @abstractmethod
    async def delete(self, path: str) -> None:
        pass
