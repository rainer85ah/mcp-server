import json
import httpx
import logging
from os import getenv
from agents.chat import general_mcp


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

# === Tool: General QA ===
@general_mcp.tool()
async def ask_question_tool(question: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(prompt=f"Respond to the following question: {question}", model=model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Classification ===
@general_mcp.tool()
async def classify_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    result = await call_ollama(f"Classify the following text into a category:\n{text}", model).__anext__()
    return result or "⚠️ No answer returned from model."

# === Tool: Sentiment Analysis ===
@general_mcp.tool()
async def sentiment_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    result = await call_ollama(f"What is the sentiment of this text?\n{text}", model).__anext__()
    return result or "⚠️ No answer returned from model."

# === Tool: Text Completion ===
@general_mcp.tool()
async def complete_text_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Continue the following:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Text Generation ===
@general_mcp.tool()
async def generate_text_tool(topic: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Write a paragraph about:\n{topic}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Code Generation ===
@general_mcp.tool()
async def generate_code_tool(task: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Write Python code for this task:\n{task}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Summarization ===
@general_mcp.tool()
async def summarize_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Summarize the following text:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Translation ===
@general_mcp.tool()
async def translate_tool(text: str, language: str = "Spanish", model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Translate this to {language}:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Paraphrasing ===
@general_mcp.tool()
async def paraphrase_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Paraphrase this to sound more formal:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."

# === Tool: Instruction Following ===
@general_mcp.tool()
async def instruction_tool(task: str, model: str = DEFAULT_MODEL) -> str:
    chunks = []
    async for chunk in call_ollama(f"Give step-by-step instructions to:\n{task}", model):
        chunks.append(chunk)
    return "".join(chunks).strip() or "⚠️ No answer returned from model."
