from fastmcp import Context
from agents.code import code_mcp
from context.code import get_code_context


@code_mcp.prompt("coding-agent")
async def code_prompt(input: str, ctx: Context):
    thread = get_code_context(ctx)
    return [
        {"role": "system", "content": (
            "You are an expert programming assistant. "
            "You write, fix, and explain code using tools like code execution, analysis, and debugging. "
            "When appropriate, call tools to run or test code snippets."
        )},
        *thread,
        {"role": "user", "content": input}
    ]
