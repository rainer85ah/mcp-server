from agents.chat import chat_mcp


@chat_mcp.prompt("chat-agent")
def chat_prompt(input: str, history: list = None):
    history = history or []
    return [
        {"role": "system", "content": "You are a friendly and knowledgeable AI assistant that helps users with general queries using available tools."},
        *history,
        {"role": "user", "content": input}
    ]
