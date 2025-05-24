import asyncio
import logging
from fastmcp import FastMCP
from tools.general import *

logger = logging.getLogger("MainAgent")
mcp = FastMCP(name="MainAgent")
mcp.dependencies = []

async def main():
    logger.info(f"Mounting Sub-Agents ...")
    mcp.mount(prefix='general', server=general_mcp)

    logger.info(f"Starting Main MCP server...")
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
