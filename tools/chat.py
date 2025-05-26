import logging
from os import getenv
from agents.chat import chat_mcp
from tools.utils import call_ollama


logger = logging.getLogger(__name__)
DEFAULT_MODEL = getenv("DEFAULT_MODEL", "llama3.2:1b-instruct-q4_K_M")


# === Tool: QA ===
@chat_mcp.tool()
async def ask_question_tool(question: str, model: str = DEFAULT_MODEL) -> str:
    """Q&A with the AI model"""
    chunks = []
    async for chunk in call_ollama(prompt=f"Respond to the following question: {question}", model=model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Classification ===
@chat_mcp.tool()
async def classify_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    """AI model classification"""
    result = await call_ollama(f"Classify the following text into a category:\n{text}", model).__anext__()
    return result

# === Tool: Sentiment Analysis ===
@chat_mcp.tool()
async def sentiment_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    """AI model provides a positive or negative sentiment of a text."""
    result = await call_ollama(f"What is the sentiment of this text?\n{text}", model).__anext__()
    return result

# === Tool: Text Completion ===
@chat_mcp.tool()
async def complete_text_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    """AI model text completion"""
    chunks = []
    async for chunk in call_ollama(f"Continue the following:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Text Generation ===
@chat_mcp.tool()
async def generate_text_tool(topic: str, model: str = DEFAULT_MODEL) -> str:
    """AI model text generation"""
    chunks = []
    async for chunk in call_ollama(f"Write a paragraph about:\n{topic}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Summarization ===
@chat_mcp.tool()
async def summarize_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    """AI model summarization"""
    chunks = []
    async for chunk in call_ollama(f"Summarize the following text:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Translation ===
@chat_mcp.tool()
async def translate_tool(text: str, language: str = "Spanish", model: str = DEFAULT_MODEL) -> str:
    """AI model translation"""
    chunks = []
    async for chunk in call_ollama(f"Translate this to {language}:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Paraphrasing ===
@chat_mcp.tool()
async def paraphrase_tool(text: str, model: str = DEFAULT_MODEL) -> str:
    """AI model Paraphrase"""
    chunks = []
    async for chunk in call_ollama(f"Paraphrase this to sound more formal:\n{text}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()

# === Tool: Instruction Following ===
@chat_mcp.tool()
async def instruction_tool(task: str, model: str = DEFAULT_MODEL) -> str:
    """AI model step-by-step guide of how to"""
    chunks = []
    async for chunk in call_ollama(f"Give step-by-step instructions to:\n{task}", model):
        chunks.append(chunk)
    return "".join(chunks).strip()
