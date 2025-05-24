from fastapi import FastAPI
from fastmcp import FastMCP

# DynamicService
chat_mcp = FastMCP(
    name="ChatAgent",
    stateless_http=True,
    dependencies=[]
)

chat_api = FastAPI(name="ChatAPI")
