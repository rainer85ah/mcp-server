import logging
from os import getenv
from agents.code import code_mcp
from tools.utils import call_ollama


logger = logging.getLogger(__name__)
DEFAULT_MODEL = getenv("DEFAULT_MODEL", "llama3.2:1b-instruct-q4_K_M")


@code_mcp.tool()
def analyze_structure(files: list) -> dict:
    """
    Analyze GitHub repositories and make suggestions and improvements.
    :param files: A list of files in the repository.
    :return: A dictionary with the content organized.
    """
    py_files = [f for f in files if f['name'].endswith('.py')]
    return {
        "file_count": len(files),
        "python_files": len(py_files),
        "file_names": [f['name'] for f in py_files],
        "suggestion": "Consider modularizing large files." if len(py_files) > 10 else "Structure looks good."
    }


@code_mcp.tool()
async def generate_code_tool(prompt: str, language: str = "python", model: str = DEFAULT_MODEL) -> str:
    """
    Generate a code implementation in the specified language based on the given natural language prompt.
    """
    language = language.lower()
    instructions = {
        "python": "Respond with well-structured Python code including functions, docstrings, and comments.",
        "javascript": "Respond with idiomatic JavaScript using modern ES6+ syntax and inline comments.",
        "typescript": "Respond with TypeScript using proper type annotations and best practices.",
        "bash": "Write Bash shell script with comments explaining each major step.",
        "go": "Generate Go code with idiomatic structure and comments.",
    }

    language_instruction = instructions.get(language, f"Write code in {language} with best practices and clear structure.")
    full_prompt = (
        f"You are a professional software engineer. {language_instruction}\n\n"
        f"Task: {prompt}\n\n"
        f"--- Begin {language} code ---\n"
    )

    chunks = []
    async for chunk in call_ollama(prompt=full_prompt, model=model):
        chunks.append(chunk)

    return "".join(chunks).strip()


@code_mcp.tool()
async def fix_code_tool(code: str, model: str = DEFAULT_MODEL) -> str:
    """Fix or refactor the given code."""
    prompt = f"Fix and improve the following code:\n\n{code}"
    chunks = []
    async for chunk in call_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks).strip()


@code_mcp.tool()
async def explain_code_tool(code: str, model: str = DEFAULT_MODEL) -> str:
    """Explain the purpose and logic of the given code."""
    prompt = f"Explain this code clearly:\n\n{code}"
    chunks = []
    async for chunk in call_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks).strip()


@code_mcp.tool()
async def write_tests_tool(code: str, language: str = "python", model: str = DEFAULT_MODEL) -> str:
    """Generate unit tests for the provided code."""
    prompt = f"Write unit tests for this {language} code:\n\n{code}"
    chunks = []
    async for chunk in call_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks).strip()


@code_mcp.tool()
async def debug_code_tool(code: str, model: str = DEFAULT_MODEL) -> str:
    """Find bugs or logical errors in the provided code."""
    prompt = f"Find bugs or errors in the following code:\n\n{code}"
    chunks = []
    async for chunk in call_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks).strip()


@code_mcp.tool()
async def generate_function_docstring_tool(code: str, model: str = DEFAULT_MODEL) -> str:
    """Generate a docstring for the provided function."""
    prompt = f"Write a clear docstring for this function:\n\n{code}"
    chunks = []
    async for chunk in call_ollama(prompt, model):
        chunks.append(chunk)
    return "".join(chunks).strip()
