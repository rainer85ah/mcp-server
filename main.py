from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp import FastMCP
from api.v1.chat import router as chat_router
from api.v1.code import router as code_router
from agents.chat import chat_mcp
from agents.code import code_mcp
from context.lifespan_context import LifespanContext
from tools.chat import *
from tools.code import *
from prompts.chat import *
from resources.chat import *
from resources.chat_templates import *
from resources.code import *
from resources.code_templates import *
from prompts.coding import *
from fastapi.middleware.cors import CORSMiddleware
from utils.logger_config import configure_logger


logger = configure_logger("MainAgent")
logger.info("Starting Main MCP server ...")

@asynccontextmanager
async def lifespan_context(app):
    lifespan = LifespanContext()
    await lifespan.startup()
    app.state.lifespan = lifespan

    try:
        yield
    finally:
        await lifespan.shutdown()

mcp = FastMCP(
    name="MainAgent",
    instructions="Coordinator for sub-agents.",
    dependencies=[],
)

mcp.lifespan_context = lifespan_context
logger.info("Mounting Sub-Agents ...")
mcp.mount(prefix='chat', server=chat_mcp)
mcp.mount(prefix='code', server=code_mcp)
mcp_app = mcp.http_app(path='/mcp')

app = FastAPI(title="MCP API", lifespan=mcp_app.router.lifespan_context)
app.mount("/service", mcp_app, name="main")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(code_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific domains
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "API up!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
