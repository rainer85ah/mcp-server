from fastapi import FastAPI
from fastmcp import FastMCP


chat_mcp = FastMCP(
    name="ChatAgent",
    instructions="You're an expert personal assistant. Respond in a short, concise, and in a summary way.",
    stateless_http=True,
    dependencies=[]
)

chat_api = FastAPI(name="ChatAPI")
