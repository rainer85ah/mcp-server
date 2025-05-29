import logging
from fastmcp import Context
from agents.code import code_mcp

logger = logging.getLogger(__name__)


@code_mcp.resource("resource://code/language-instruction/{language}")
async def code_language_instruction(language: str, ctx: Context) -> str:
    try:
        instructions = {
            "python": "Use idiomatic Python. Include functions, docstrings, and clear comments.",
            "javascript": "Use ES6+ syntax. Add inline comments.",
            "typescript": "Use type annotations. Follow TS best practices.",
            "bash": "Use safe Bash with comments for each command.",
            "go": "Write idiomatic Go code with clear structure and documentation.",
        }
        return instructions.get(language.lower(), f"Write clean and idiomatic code in {language}.")
    except Exception as e:
        logger.exception(f"Failed to generate language instruction for: {language}")
        return ""


@code_mcp.resource("resource://code/refactor-prompt/{code}")
async def code_refactor_prompt(code: str, ctx: Context) -> str:
    try:
        return f"Refactor and improve the following code:\n\n{code}"
    except Exception as e:
        logger.exception("Failed to generate refactor prompt")
        return ""


@code_mcp.resource("resource://code/test-prompt/{language}")
async def code_test_prompt(language: str, code: str = "", ctx: Context = None) -> str:
    try:
        return f"Write unit tests for this {language} code:\n\n{code}"
    except Exception as e:
        logger.exception("Failed to generate test prompt")
        return ""


@code_mcp.resource("resource://code/docstring-prompt/{function_code}")
async def code_docstring_prompt(function_code: str, ctx: Context) -> str:
    try:
        return f"Generate a helpful and clear docstring for the following function:\n\n{function_code}"
    except Exception as e:
        logger.exception("Failed to generate docstring prompt")
        return ""


@code_mcp.resource("resource://code/debug-prompt/{code}")
async def code_debug_prompt(code: str, ctx: Context) -> str:
    try:
        return f"Find bugs or issues in this code and explain them:\n\n{code}"
    except Exception as e:
        logger.exception("Failed to generate debug prompt")
        return ""


@code_mcp.resource("resource://code/explain-prompt/{code}")
async def code_explain_prompt(code: str, ctx: Context) -> str:
    try:
        return f"Explain the following code snippet in plain English:\n\n{code}"
    except Exception as e:
        logger.exception("Failed to generate explain prompt")
        return ""
