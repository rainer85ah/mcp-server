from fastapi import FastAPI
from fastmcp import FastMCP

# DynamicService
general_mcp = FastMCP(name="GeneralAgent")

general_api = FastAPI(name="GeneralAPI")
