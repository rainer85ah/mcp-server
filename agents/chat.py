from os import getenv
from typing import Literal, cast
from mcp.server.fastmcp import FastMCP
from tools.chat import greet_user, summarize_conversation, get_current_time


chat_agent = FastMCP(
    "ChatAgent",
    instructions="You're a helpful conversational assistant.",
    stateless_http=True,
    dependencies=[greet_user, summarize_conversation, get_current_time],
)


if __name__ == "__main__":
    TransportType = Literal["stdio", "streamable-http"]
    transport = cast(TransportType, getenv("MCP_TRANSPORT", "stdio"))
    chat_agent.run(transport=transport)
