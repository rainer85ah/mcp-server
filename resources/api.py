import aiohttp
import asyncio
from resources.base import DataSource
from typing import Optional, Dict, Any
from mcp.server.fastmcp.server import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from aiohttp import ClientResponseError, ClientConnectionError, ClientTimeout



class RestAPIs(DataSource):
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self.headers, timeout=self.timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientConnectionError, ClientResponseError)),
        reraise=True
    )
    async def read(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        session = await self._get_session()
        try:
            async with session.get(url, params=params, **kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except ClientResponseError as e:
            logger.error(f"HTTP error during GET {url}: {e.status} {e.message}")
            raise
        except asyncio.TimeoutError:
            logger.error(f"Timeout during GET {url}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during GET {url}: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientConnectionError, ClientResponseError)),
        reraise=True
    )
    async def write(self, endpoint: str, payload: Dict[str, Any], method: str = "POST", **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        session = await self._get_session()
        method = method.upper()
        try:
            async with session.request(method, url, json=payload, **kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except ClientResponseError as e:
            logger.error(f"HTTP error during {method} {url}: {e.status} {e.message}")
            raise
        except asyncio.TimeoutError:
            logger.error(f"Timeout during {method} {url}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during {method} {url}: {e}")
            raise
