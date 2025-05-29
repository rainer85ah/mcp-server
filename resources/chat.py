from fastmcp import Context
from agents.chat import chat_mcp


@chat_mcp.resource("resource://chat/help")
async def chat_help(ctx: Context) -> str:
    return (
        "Welcome to the Chat Tool!\n\n"
        "You can ask me to fetch data from APIs, databases, or the web.\n"
        "Try commands like:\n"
        "- 'Get website content from URL'\n"
        "- 'Fetch API data from endpoint'\n"
        "- 'Read local file at path'\n"
        "- 'Access MongoDB or PostgreSQL data'\n"
        "- 'Get S3 file contents'\n"
    )

@chat_mcp.resource("resource://chat/status")
async def chat_status(ctx: Context) -> str:
    return "✅ Chat tool is online and ready to assist you."

@chat_mcp.resource("resource://chat/tools")
async def chat_tools(ctx: Context) -> list:
    return [
        "Website fetcher",
        "API JSON fetcher",
        "GitHub repo reader",
        "MongoDB document fetcher",
        "PostgreSQL reader",
        "S3 file reader",
        "Local file reader",
    ]

@chat_mcp.resource("resource://chat/version")
async def chat_version(ctx: Context) -> str:
    return "Chat Tool Agent v1.0.0"

@chat_mcp.resource("resource://chat/acknowledgments")
async def chat_acknowledgments(ctx: Context) -> str:
    return (
        "This tool was built using FastMCP, powered by Python async I/O, "
        "and integrates MongoDB, PostgreSQL, AWS S3, and web scraping capabilities."
    )
