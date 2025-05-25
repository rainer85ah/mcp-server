from fastmcp import FastMCP


code_mcp = FastMCP(
    name="CodeAgent",
    instructions="You're an expert programming assistant. Write correct and efficient code.",
    stateless_http=True,
    dependencies=[]
)
