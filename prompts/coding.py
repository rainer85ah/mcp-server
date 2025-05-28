from agents.code import code_mcp


@code_mcp.prompt("coding-agent")
def code_prompt(input: str, history: list = None):
    history = history or []
    return [
        {"role": "system", "content": (
            "You are an expert programming assistant. "
            "You write, fix, and explain code using tools like code execution, analysis, and debugging. "
            "When appropriate, call tools to run or test code snippets."
        )},
        *history,
        {"role": "user", "content": input}
    ]
