import logging
from os import getenv
from fastmcp import Context
from agents.chat import chat_mcp
from tools.utils import call_ollama
from typing import Annotated


logger = logging.getLogger(__name__)
DEFAULT_MODEL = getenv("DEFAULT_MODEL", "llama3.2:1b-instruct-q4_K_M")


# === Tool: QA ===
@chat_mcp.tool(
    name="ask_question_tool",
    description="Answer a natural language question using the AI model."
)
async def ask_question_tool(
        question: Annotated[str, "The natural language question to answer."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL,
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(prompt=f"Respond to the following question: {question}", model=model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"ask_question_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Classification ===
@chat_mcp.tool(
    name="classify_tool",
    description="Classify a block of text into a predefined category."
)
async def classify_tool(
        text: Annotated[str, "Text to classify into a category."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        result = await call_ollama(f"Classify the following text into a category:\n{text}", model).__anext__()
        return result
    except Exception as e:
        logger.exception(f"classify_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Sentiment Analysis ===
@chat_mcp.tool(
    name="sentiment_tool",
    description="Analyze the sentiment of a text and classify it as positive, neutral, or negative."
)
async def sentiment_tool(
        text: Annotated[str, "Text whose sentiment is being analyzed."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        result = await call_ollama(f"What is the sentiment of this text?\n{text}", model).__anext__()
        return result
    except Exception as e:
        logger.exception(f"sentiment_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Text Completion ===
@chat_mcp.tool(
    name="complete_text_tool",
    description="Complete a partial sentence or paragraph with a coherent continuation."
)
async def complete_text_tool(
        text: Annotated[str, "Text fragment to be completed."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Continue the following:\n{text}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"complete_text_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Text Generation ===
@chat_mcp.tool(
    name="generate_text_tool",
    description="Generate a paragraph of text about a given topic."
)
async def generate_text_tool(
        topic: Annotated[str, "Topic to write about."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Write a paragraph about:\n{topic}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"generate_text_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Summarization ===
@chat_mcp.tool(
    name="summarize_tool",
    description="Summarize a long body of text into a concise summary."
)
async def summarize_tool(
        text: Annotated[str, "Text to summarize."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Summarize the following text:\n{text}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"summarize_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Translation ===
@chat_mcp.tool(
    name="translate_tool",
    description="Translate a given text into another language."
)
async def translate_tool(
        text: Annotated[str, "Text to translate."],
        language: Annotated[str, "Target language."] = "Spanish",
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Translate this to {language}:\n{text}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"translate_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Paraphrasing ===
@chat_mcp.tool(
    name="paraphrase_tool",
    description="Rephrase a given text to sound more formal or fluent."
)
async def paraphrase_tool(
        text: Annotated[str, "Text to paraphrase."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Paraphrase this to sound more formal:\n{text}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"paraphrase_tool failed: {e}")
        return "An error occurred while processing the request."

# === Tool: Instruction Following ===
@chat_mcp.tool(
    name="instruction_tool",
    description="Provide a step-by-step guide to accomplish a given task."
)
async def instruction_tool(
        task: Annotated[str, "The task you want instructions for."],
        model: Annotated[str, "LLM model to use."] = DEFAULT_MODEL
) -> str:
    try:
        chunks = []
        async for chunk in call_ollama(f"Give step-by-step instructions to:\n{task}", model):
            chunks.append(chunk)
        return "".join(chunks).strip()
    except Exception as e:
        logger.exception(f"instruction_tool failed: {e}")
        return "An error occurred while processing the request."

