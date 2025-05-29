import logging
from os import getenv
from agents.code import code_mcp
from tools.utils import call_ollama
from typing import Annotated


logger = logging.getLogger(__name__)
DEFAULT_MODEL = getenv("DEFAULT_MODEL", "llama3.2:1b-instruct-q4_K_M")


@code_mcp.tool(

    name="analyze_structure",
    description="Analyze the structure of a repository to count files and make structure suggestions."
)
def analyze_structure(
        files: Annotated[list, "A list of file metadata from a GitHub repository."]
) -> dict:
    try:
        py_files = [f for f in files if f['name'].endswith('.py')]
        return {
            "file_count": len(files),
            "python_files": len(py_files),
            "file_names": [f['name'] for f in py_files],
            "suggestion": "Consider modularizing large files." if len(py_files) > 10 else "Structure looks good."
        }
    except Exception as e:
        logger.exception(f"analyze_structure failed: {e}")
        return {"error": "Failed to analyze structure."}

@code_mcp.tool(
    name="generate_code",
    description="Generate source code in the specified language based on a prompt."
)
async def generate_code_tool(
        prompt: Annotated[str, "Natural language prompt describing what to code."],
        language: Annotated[str, "Programming language."] = "python",
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        language = language.lower()
        instructions = {
            "python": "Respond with well-structured Python code including functions, docstrings, and comments.",
            "javascript": "Respond with idiomatic JavaScript using modern ES6+ syntax and inline comments.",
            "typescript": "Respond with TypeScript using proper type annotations and best practices.",
            "bash": "Write Bash shell script with comments explaining each major step.",
            "go": "Generate Go code with idiomatic structure and comments."
        }
        instruction = instructions.get(language, f"Write code in {language} with best practices and clear structure.")
        full_prompt = f"You are a professional software engineer. {instruction}\n\nTask: {prompt}\n\n--- Begin {language} code ---\n"
        chunks = []
        async for chunk in call_ollama(prompt=full_prompt, model=model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"generate_code_tool failed: {e}")
        return "An error occurred while generating code."

@code_mcp.tool(
    name="fix_code_tool",
    description="Fix and refactor provided code."
)
async def fix_code_tool(
        code: Annotated[str, "Code snippet to fix or refactor."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        prompt = f"Fix and improve the following code:\n\n{code}"
        chunks = []
        async for chunk in call_ollama(prompt, model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"fix_code_tool failed: {e}")
        return "An error occurred while fixing the code."

@code_mcp.tool(
    name="explain_code_tool",
    description="Explain the logic and purpose of a given code snippet."
)
async def explain_code_tool(
        code: Annotated[str, "Code snippet to explain."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        prompt = f"Explain this code clearly:\n\n{code}"
        chunks = []
        async for chunk in call_ollama(prompt, model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"explain_code_tool failed: {e}")
        return "An error occurred while explaining the code."

@code_mcp.tool(
    name="write_tests_tool",
    description="Generate unit tests for the given code."
)
async def write_tests_tool(
        code: Annotated[str, "Code to generate unit tests for."],
        language: Annotated[str, "Programming language."] = "python",
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        prompt = f"Write unit tests for this {language} code:\n\n{code}"
        chunks = []
        async for chunk in call_ollama(prompt, model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"write_tests_tool failed: {e}")
        return "An error occurred while generating unit tests."

@code_mcp.tool(
    name="debug_code_tool",
    description="Detect bugs and logical errors in the provided code."
)
async def debug_code_tool(
        code: Annotated[str, "Code to debug."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        prompt = f"Find bugs or errors in the following code:\n\n{code}"
        chunks = []
        async for chunk in call_ollama(prompt, model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"debug_code_tool failed: {e}")
        return "An error occurred while debugging the code."

@code_mcp.tool(
    name="generate_function_docstring_tool",
    description="Generate a clear and informative docstring for the given function."
)
async def generate_function_docstring_tool(
        code: Annotated[str, "Function code to document."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        prompt = f"Write a clear docstring for this function:\n\n{code}"
        chunks = []
        async for chunk in call_ollama(prompt, model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"generate_function_docstring_tool failed: {e}")
        return "An error occurred while generating a docstring."
