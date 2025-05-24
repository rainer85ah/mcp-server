import asyncio
import logging

from fastapi import FastAPI
from fastmcp import FastMCP
from tools.general import *
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger("MainAgent")

mcp = FastMCP(name="MainAgent")
mcp.mount(prefix='general', server=general_mcp)
mcp.dependencies = []
mcp_app = mcp.http_app(path='/mcp')
app = FastAPI(title="MainAgent API")
app.mount("/mcp", mcp.http_app())


async def main():
    logger.info(f"Running MCP Server ...")
    try:
        await mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port="8000",
            path="/mcp"
        )
    except Exception as e:
        logger.exception("Fatal error in MCP server")
    finally:
        logger.info("MCP server shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
