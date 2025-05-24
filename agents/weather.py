import asyncio
import contextlib
from os import getenv
from typing import Literal, cast
from dotenv import load_dotenv
from fastapi import FastAPI
from fastmcp import FastMCP
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from context.context import AppContext


load_dotenv()

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    try:
        yield AppContext()
    finally:
        pass

mcp = FastMCP(
    name="Weather MCP Server",
    instructions="This server provides weather information.",
    lifespan=lifespan,
)


app = FastAPI()
app.mount("/weather", )

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by ID."""
    # The {user_id} in the URI is extracted and passed to this function
    return {"id": user_id, "name": f"User {user_id}", "status": "active"}

@mcp.prompt()
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"

async def main():
    TransportType = Literal["stdio", "streamable-http"]
    transport = cast(TransportType, getenv("MCP_TRANSPORT", "stdio"))
    await mcp.run_async(transport=transport, host="127.0.0.1", port=9000, path="/weather", )


if __name__ == "__main__":
    asyncio.run(main())

