import asyncio
import logging
from fastmcp import FastMCP
from agents.chat import chat_mcp
from agents.code import code_mcp
from tools.chat import *
from tools.code import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MainAgent")


mcp = FastMCP(
    name="MainAgent",
    instructions="You are the main model-context-protocol server which manages sub-agents who are experts in different topics.",
    dependencies=[],
)


async def main():
    logger.info("Mounting Sub-Agents ...")
    logger.info(f"chat_mcp: {chat_mcp}")
    mcp.mount(prefix='chat', server=chat_mcp)
    logger.info(f"code_mcp: {code_mcp}")
    mcp.mount(prefix='code', server=code_mcp)

    logger.info(f"Starting Main MCP server...")
    try:
        await mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=8000,
            path="/mcp"
        )
    except Exception as e:
        logger.exception("Fatal error in MCP server")
    finally:
        logger.info("MCP server shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())
