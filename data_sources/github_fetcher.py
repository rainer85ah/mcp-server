import httpx
from utils.retries import http_retry
from utils.logger_config import configure_logger


logger = configure_logger("GitHubFetcher")


class GitHubFetcher:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str = None):
        self.headers = {"Authorization": f"token {token}"} if token else {}

    @http_retry()
    async def get_repo_contents(self, owner: str, repo: str, path: str = "") -> list:
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
