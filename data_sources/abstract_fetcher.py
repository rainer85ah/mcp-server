from abc import ABC, abstractmethod
from typing import Dict


class BaseFetcher(ABC):

    @abstractmethod
    async def fetch(self, url: str, params: Dict = None) -> Dict:
        pass
