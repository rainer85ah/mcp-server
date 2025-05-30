"""
This file (server.py) is used for testing new changes to the main.py file and as a backup.
"""
import asyncio
import logging
from fastapi import FastAPI
from fastmcp import FastMCP
from api.v1.chat import router as chat_router
from api.v1.code import router as code_router
from agents.chat import chat_mcp
from agents.code import code_mcp
from tools.chat import *
from tools.code import *


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MainAgent")


logger.info(f"Starting Main MCP server ...")
mcp = FastMCP(
    name="MainAgent",
    instructions="Coordinator for sub-agents.",
    dependencies=[],
)

logger.info("Mounting Sub-Agents ...")
logger.info(f"chat_mcp: {chat_mcp}")
mcp.mount(prefix='chat', server=chat_mcp)
logger.info(f"code_mcp: {code_mcp}")
mcp.mount(prefix='code', server=code_mcp)
mcp_app = mcp.http_app(path='/mcp')

app = FastAPI(title="MCP API", lifespan=mcp_app.router.lifespan_context)
app.mount("/service", mcp_app, name="main")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(code_router, prefix="/api/v1")

@app.get("/")
async def home():
    return {"status": "API up!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
