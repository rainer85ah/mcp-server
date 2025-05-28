from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseDB(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def read(self, filter_query: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def write(self, document: Dict[str, Any], **kwargs) -> None:
        pass

    @abstractmethod
    async def update(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False) -> int:
        pass

    @abstractmethod
    async def delete(self, filter_query: Dict[str, Any]) -> int:
        pass
