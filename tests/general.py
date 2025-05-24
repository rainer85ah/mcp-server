import pytest
import pytest_asyncio
from fastmcp.client import Client
from agents.general import general_mcp
from main import logger

pytestmark = pytest.mark.asyncio

# --- Test matrix ---
tool_tests = [
    ("ask_question_tool", {"question": "What is the capital of France?"}),
    ("complete_text_tool", {"text": "Once upon a time"}),
    ("generate_text_tool", {"topic": "The benefits of walking"}),
    ("generate_code_tool", {"task": "Write a Python function to reverse a string"}),
    ("summarize_tool", {"text": "This is a long paragraph that needs summarizing..."}),
    ("translate_tool", {"text": "Hello, world!", "language": "French"}),
    ("paraphrase_tool", {"text": "This is a basic sentence."}),
    ("classify_tool", {"text": "The stock price fell sharply today."}),
    ("sentiment_tool", {"text": "I absolutely love this!"}),
    ("instruction_tool", {"task": "Change a flat tire"})
]

# --- Shared client fixture ---
@pytest_asyncio.fixture
async def mock_client():
    tools = await general_mcp.get_tools()
    logger.info(f"Available tools: {list(tools.keys())}")

    async with Client(general_mcp) as client:
        yield client

# --- Parameterized test ---
@pytest.mark.parametrize("tool_name, inputs", tool_tests)
async def test_llm_tools(mock_client, tool_name, inputs):
    result = await mock_client.call_tool(tool_name, inputs)
    print("Inference result:", result[0].text)
    assert result[0].text  # Check exact value or type
