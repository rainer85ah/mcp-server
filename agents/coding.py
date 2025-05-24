from os import getenv
from typing import Literal, cast
from mcp.server.fastmcp import FastMCP
from tools.coding import generate_code


coding_agent = FastMCP(
    "CodeAgent",
    instructions="You're an expert programming assistant. Write correct and efficient code.",
    dependencies=[generate_code],
)


if __name__ == "__main__":
    TransportType = Literal["stdio", "streamable-http"]
    transport = cast(TransportType, getenv("MCP_TRANSPORT", "stdio"))
    coding_agent.run(transport=transport)