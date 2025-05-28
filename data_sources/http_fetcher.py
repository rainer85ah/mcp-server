import httpx
from bs4 import BeautifulSoup
from utils.retries import http_retry
from data_sources.abstract_fetcher import BaseFetcher
from utils.logger_config import configure_logger


logger = configure_logger("HTTPFetcher")


class WebsiteFetcher(BaseFetcher):

    @http_retry()
    async def fetch(self, url: str, params: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                return {"title": soup.title.string if soup.title else None}
            except Exception as e:
                logger.error(f"Scrape failed: {url}", exc_info=e)
                raise
