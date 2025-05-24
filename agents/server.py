from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from os import getenv
from typing import Literal, cast
from dotenv import load_dotenv
from fastapi import FastAPI
from fastmcp import FastMCP
from agents.chat import dynamic_mcp
from api.v1.chat import router
from context.context import AppContext


load_dotenv()


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    try:
        yield AppContext()
    finally:
        pass


# Mount subserver (synchronous operation)
main_mcp = FastMCP(name="MainMCPServer")
main_mcp.mount("items", dynamic_mcp)

app = FastAPI(name="MCP API")
app.include_router(router, tags=["items"])

@app.get("/")
async def home():
    return "API Up!"


async def main():
    mcp = FastMCP.from_fastapi(app=app)
    TransportType = Literal["stdio", "streamable-http"]
    transport = cast(TransportType, getenv("MCP_TRANSPORT", "stdio"))
    await mcp.run_async(transport=transport)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
