import pytest
from tools.chat import DEFAULT_MODEL


@pytest.mark.asyncio
async def test_ask_question_endpoint(async_client):
    response = await async_client.get("/api/v1/chat/ask", params={
        "question": "What is FastAPI?",
        "model": DEFAULT_MODEL
    })

    assert response.status_code == 200
    json = response.json()
    assert "result" in json
    assert isinstance(json["result"], str)
    assert json["result"].strip() != ""

