from asyncio import get_event_loop
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop

# Sync test client for synchronous tests
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# Async test client for async tests, bind to FastAPI app and base URL
@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(base_url="http://0.0.0.0") as client:
        yield client
