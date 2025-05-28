from fastmcp import Context
from agents.chat import chat_mcp
from context.chat import get_chat_context


@chat_mcp.prompt("chat-agent")
async def chat_prompt(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return [
        {"role": "system", "content": "You are a friendly and knowledgeable AI assistant that helps users with general queries using available tools."},
        *history,
        {"role": "user", "content": input}
    ]
