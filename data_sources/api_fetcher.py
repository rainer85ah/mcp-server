import httpx
from utils.retries import http_retry
from data_sources.abstract_fetcher import BaseFetcher
from utils.logger_config import configure_logger


logger = configure_logger("HttpFetcher")


class HttpFetcher(BaseFetcher):

    @http_retry()
    async def fetch(self, url: str, params: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Fetch failed: {url}", exc_info=e)
                raise
