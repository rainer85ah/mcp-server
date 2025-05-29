from fastmcp import Context
from agents.code import code_mcp


@code_mcp.resource("resource://code/status")
async def code_status(ctx: Context) -> str:
    return "🧠 Code tools are online and ready for use."

@code_mcp.resource("resource://code/summary")
async def code_summary(ctx: Context) -> str:
    return (
        "This code agent provides tools for:\n"
        "- Code generation\n"
        "- Code explanation\n"
        "- Debugging and refactoring\n"
        "- Writing unit tests\n"
        "- Generating docstrings\n"
        "- Analyzing project structure\n"
    )

@code_mcp.resource("resource://code/tool_list")
async def code_tool_list(ctx: Context) -> list:
    return [
        "analyze_structure",
        "generate_code",
        "fix_code_tool",
        "explain_code_tool",
        "write_tests_tool",
        "debug_code_tool",
        "generate_function_docstring_tool"
    ]

@code_mcp.resource("resource://code/version")
async def code_version(ctx: Context) -> str:
    return "Code Tool Agent v1.0.0 – Powered by LLaMA3 and FastMCP"

@code_mcp.resource("resource://code/help")
async def code_help(ctx: Context) -> str:
    return (
        "🛠️ Code Tool Help Menu:\n\n"
        "- Use `generate_code` to create new code.\n"
        "- Use `fix_code_tool` to refactor and clean up code.\n"
        "- Use `explain_code_tool` for logic breakdowns.\n"
        "- Use `write_tests_tool` to create unit tests.\n"
        "- Use `debug_code_tool` to find bugs.\n"
        "- Use `generate_function_docstring_tool` for documentation help.\n"
        "- Use `analyze_structure` for repo insights.\n"
    )
