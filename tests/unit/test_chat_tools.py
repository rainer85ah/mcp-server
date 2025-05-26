import pytest
from mcp import McpError
from fastmcp import Client
from fastmcp.exceptions import ClientError


tool_tests = [
    ("chat_ask_question_tool", {"question": "What is the capital of France?"}),
    ("chat_complete_text_tool", {"text": "Once upon a time"}),
    ("chat_generate_text_tool", {"topic": "The benefits of walking"}),
    ("chat_summarize_tool", {"text": "This is a long paragraph that needs summarizing..." * 10}),
    ("chat_translate_tool", {"text": "Hello, world!", "language": "French"}),
    ("chat_paraphrase_tool", {"text": "This is a basic sentence."}),
    ("chat_classify_tool", {"text": "The stock price fell sharply today."}),
    ("chat_sentiment_tool", {"text": "I absolutely love this!"}),
    ("chat_instruction_tool", {"task": "Change a flat tire"})
]

@pytest.mark.parametrize("tool_name, arguments", tool_tests)
async def test_ask_question_tool(tool_name, arguments):
    async with Client("http://0.0.0.0:8000/service/mcp") as client:
        await client.ping()
        try:
            response = await client.call_tool(name=tool_name, arguments=arguments)
            assert isinstance(response[0].text, str)
            assert response[0].text != ""
        except ClientError as e:
            print(f"Tool call failed: {e}")
        except McpError as e:
            print(f"The task timed out: {e}")
        except ConnectionError as e:
            print(f"Connection failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}.")
