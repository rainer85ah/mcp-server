import json
import httpx
import logging
from os import getenv
from agents.code import code_mcp


logger = logging.getLogger(__name__)
DEFAULT_MODEL = getenv("DEFAULT_MODEL")
OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL")


async def call_ollama(prompt: str, model: str):
    received = False
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                    "POST",
                    f"{OLLAMA_BASE_URL}/api/generate",
                    json={
                        "stream": True,
                        "model": model,
                        "prompt": prompt,
                    }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.strip():
                        if line.startswith("data:"):
                            line = line.removeprefix("data:").strip()
                        try:
                            data = json.loads(line)
                            content = data.get("response", "")
                            if content:
                                received = True
                                yield content
                        except json.JSONDecodeError:
                            logger.warning(f"Non-JSON response chunk: {line.strip()}")
        if not received:
            yield "⚠️ No content received from model."
    except httpx.TimeoutException:
        logger.warning("Timeout communicating with Ollama.")
        yield "⏱️ Timeout: The model took too long to respond."
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text.strip()}")
        yield f"❌ HTTP {e.response.status_code}: {e.response.text.strip()}"
    except httpx.RequestError as e:
        logger.error(f"Network error while calling Ollama: {e}")
        yield f"🚫 Request error: {str(e)}"
    except Exception as e:
        logger.exception("Unexpected error calling Ollama")
        yield f"💥 Unexpected error: {str(e)}"


@code_mcp.tool()
async def generate_code_tool(prompt: str, language: str = "python", model: str = DEFAULT_MODEL) -> str:
    """
    Generate a code implementation in the specified language based on the given natural language prompt.
    Includes basic structure, comments, and function-level explanations where appropriate.
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
