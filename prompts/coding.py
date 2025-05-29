from agents.code import code_mcp
from mcp.server.fastmcp import Context


@code_mcp.prompt("generate_code", description="Prompt to generate idiomatic source code from a natural prompt.")
def prompt_generate_code(prompt: str, language: str, ctx: Context):
    instruction_map = {
        "python": "Respond with well-structured Python code including functions, docstrings, and comments.",
        "javascript": "Respond with idiomatic JavaScript using modern ES6+ syntax and inline comments.",
        "typescript": "Respond with TypeScript using proper type annotations and best practices.",
        "bash": "Write Bash shell script with comments explaining each major step.",
        "go": "Generate Go code with idiomatic structure and comments."
    }
    instruction = instruction_map.get(language.lower(), f"Write {language} code using best practices and clear structure.")
    system = f"You are a professional {language} engineer. {instruction}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]

@code_mcp.prompt("fix_code_tool", description="Prompt to refactor and correct code issues.")
def prompt_fix_code(code: str, ctx: Context):
    return [
        {"role": "system", "content": "You are a senior engineer skilled in debugging and refactoring."},
        {"role": "user", "content": f"Fix and improve the following code:\n\n{code}"}
    ]

@code_mcp.prompt("explain_code_tool", description="Prompt to explain what a code snippet does.")
def prompt_explain_code(code: str, ctx: Context):
    return [
        {"role": "system", "content": "You are a teacher explaining code to beginners."},
        {"role": "user", "content": f"Explain this code clearly:\n\n{code}"}
    ]

@code_mcp.prompt("write_tests_tool", description="Prompt to generate test cases for the given code.")
def prompt_write_tests(code: str, language: str, ctx: Context):
    return [
        {"role": "system", "content": f"Write unit tests for the following {language} code."},
        {"role": "user", "content": code}
    ]

@code_mcp.prompt("debug_code_tool", description="Prompt to find bugs and logical errors in code.")
def prompt_debug_code(code: str, ctx: Context):
    return [
        {"role": "system", "content": "You are an expert debugger. Identify any bugs or issues in this code."},
        {"role": "user", "content": code}
    ]

@code_mcp.prompt("generate_function_docstring_tool", description="Prompt to write a docstring for a function.")
def prompt_docstring(code: str, ctx: Context):
    return [
        {"role": "system", "content": "You are a documentation expert. Generate a clean and informative docstring."},
        {"role": "user", "content": f"Write a docstring for this function:\n\n{code}"}
    ]
