from fastapi import APIRouter, HTTPException, Depends
from models.types import CodePrompt, CodeInput
from agents.code import code_mcp
import logging
from typing import Callable, Awaitable, TypeVar, Any, Coroutine
from tools.code import (
    generate_code_tool, fix_code_tool, explain_code_tool,
    write_tests_tool, debug_code_tool, generate_function_docstring_tool
)

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/code",
    tags=["Code Tools"],
    responses={500: {"description": "Internal Server Error"}}
)

R = TypeVar("R")


def async_wrapper(fn: Callable[..., Coroutine[Any, Any, R]]) -> Callable[..., Coroutine[Any, Any, dict]]:
    """
    A decorator to wrap async functions with error handling and unified response format.
    """
    async def wrapper(*args, **kwargs) -> dict:
        try:
            result = await fn(*args, **kwargs)
            return {"result": result}
        except Exception as e:
            logger.exception(f"[{fn.__name__}] Tool error: {e}")
            raise HTTPException(status_code=500, detail="Tool failed. See logs.")
    return wrapper


@router.get(
    "/",
    summary="List available coding tools",
    description="Returns the list of available AI-powered coding tools.",
    response_description="A dictionary listing the available code tools."
)
async def list_code_tools():
    tools = await code_mcp.get_tools()
    return {"tools": str(tools)}


@router.post(
    "/generate",
    summary="Generate code from a prompt",
    description="Generates code based on a natural language prompt, optional programming language, and model.",
    response_model=dict,
    response_description="The generated source code."
)
@async_wrapper
async def generate_code(payload: CodePrompt):
    return await generate_code_tool(prompt=payload.prompt, language=payload.language, model=payload.model)


@router.post(
    "/fix",
    summary="Fix or refactor code",
    description="Refactors or fixes provided code using an AI model.",
    response_model=dict,
    response_description="The refactored or fixed code."
)
@async_wrapper
async def fix_code(payload: CodeInput):
    return await fix_code_tool(code=payload.code, model=payload.model)


@router.post(
    "/explain",
    summary="Explain code logic",
    description="Provides a human-readable explanation of what the code does.",
    response_model=dict,
    response_description="Explanation of the code's behavior."
)
@async_wrapper
async def explain_code(payload: CodeInput):
    return await explain_code_tool(code=payload.code, model=payload.model)


@router.post(
    "/test",
    summary="Generate tests for code",
    description="Creates unit tests for the given source code using AI.",
    response_model=dict,
    response_description="The generated test code."
)
@async_wrapper
async def write_tests(payload: CodeInput):
    return await write_tests_tool(code=payload.code, language=payload.language, model=payload.model)


@router.post(
    "/debug",
    summary="Debug code",
    description="Analyzes code for bugs and returns potential fixes.",
    response_model=dict,
    response_description="Debug suggestions or fixes for the code."
)
@async_wrapper
async def debug_code(payload: CodeInput):
    return await debug_code_tool(code=payload.code, model=payload.model)


@router.post(
    "/docstring",
    summary="Generate docstring for a function",
    description="Generates a descriptive docstring for a given Python function.",
    response_model=dict,
    response_description="The generated docstring."
)
@async_wrapper
async def generate_docstring(payload: CodeInput):
    return await generate_function_docstring_tool(code=payload.code, model=payload.model)

