import json
import httpx
import logging
from os import getenv


logger = logging.getLogger(__name__)
OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://192.168.1.20:11434")


async def call_ollama(prompt: str, model: str):
    received = False
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.info(f"OLLAMA_BASE_URL: {OLLAMA_BASE_URL}.")
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

