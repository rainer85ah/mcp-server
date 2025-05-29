from pydantic import Field
from agents.code import code_mcp
from fastmcp.prompts.prompt import Message


def build_prompt(system: str, user: str) -> list[Message]:
    return [
        Message(role="system", content=system),
        Message(role="user", content=user)
    ]


@code_mcp.prompt(
    "generate_code",
    description="Prompt to generate idiomatic source code from a natural prompt."
)
def prompt_generate_code(
        task_description: str = Field(description="The natural language description of code to generate"),
        language: str = Field(default="python", description="Target programming language"),
) -> list[Message]:
    instruction_map = {
        "python": "Respond with well-structured Python code including functions, docstrings, and comments.",
        "javascript": "Respond with idiomatic JavaScript using modern ES6+ syntax and inline comments.",
        "typescript": "Respond with TypeScript using proper type annotations and best practices.",
        "bash": "Write a Bash shell script with comments explaining each major step.",
        "go": "Generate Go code with idiomatic structure and comments."
    }
    system_message = instruction_map.get(
        language.lower(),
        f"Write {language} code using best practices and clear structure."
    )
    return build_prompt(system_message, task_description)


@code_mcp.prompt(
    "fix_code_tool",
    description="Prompt to refactor and correct code issues."
)
def prompt_fix_code(
        code: str = Field(description="Code snippet to fix or refactor.")
) -> list[Message]:
    return build_prompt(
        "You are a senior engineer skilled in debugging and refactoring.",
        f"Fix and improve the following code:\n\n{code}"
    )


@code_mcp.prompt(
    "explain_code_tool",
    description="Prompt to explain what a code snippet does."
)
def prompt_explain_code(
        code: str = Field(description="Code snippet to explain.")
) -> list[Message]:
    return build_prompt(
        "You are a teacher explaining code to beginners.",
        f"Explain this code clearly:\n\n{code}"
    )


@code_mcp.prompt(
    "write_tests_tool",
    description="Prompt to generate test cases for the given code."
)
def prompt_write_tests(
        code: str = Field(description="Code to generate unit tests for."),
        language: str = Field(description="Target programming language.")
) -> list[Message]:
    return build_prompt(
        f"Write unit tests for the following {language} code.",
        code
    )


@code_mcp.prompt(
    "debug_code_tool",
    description="Prompt to find bugs and logical errors in code."
)
def prompt_debug_code(
        code: str = Field(description="Code to debug.")
) -> list[Message]:
    return build_prompt(
        "You are an expert debugger. Identify any bugs or issues in this code.",
        code
    )


@code_mcp.prompt(
    "generate_function_docstring_tool",
    description="Prompt to write a docstring for a function."
)
def prompt_docstring(
        code: str = Field(description="Function code to document.")
) -> list[Message]:
    return build_prompt(
        "You are a documentation expert. Generate a clean and informative docstring.",
        f"Write a docstring for this function:\n\n{code}"
    )
