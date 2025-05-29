import logging
from typing import Optional, Callable, Awaitable, Coroutine, Any
from fastapi import APIRouter, HTTPException, Query
from models.types import ChatResponse
from tools.chat import (
    chat_mcp, ask_question_tool, classify_tool, sentiment_tool,
    complete_text_tool, generate_text_tool, summarize_tool,
    translate_tool, paraphrase_tool, instruction_tool, DEFAULT_MODEL
)

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/chat",
    tags=["Chat Tools"],
    responses={500: {"description": "Internal Server Error"}}
)


def safe_call(fn: Callable[..., Coroutine[Any, Any, ChatResponse]]):
    """
    Decorator for safely executing chat tool functions with error logging.
    """
    async def wrapper(*args, **kwargs):
        try:
            return {"result": await fn(*args, **kwargs)}
        except Exception as e:
            logger.exception(f"Chat tool error in {fn.__name__}: {e}")
            raise HTTPException(status_code=500, detail="Chat tool failed")
    return wrapper


@router.get(
    "/",
    summary="List available chat tools",
    description="Returns the list of chat tools currently supported.",
    response_description="A list of available chat tools."
)
async def get_chat_tools():
    response = await chat_mcp.get_tools()
    return {"status": str(response)}


@router.get(
    "/ask",
    summary="Ask a question",
    description="Asks a question to the LLM and returns an intelligent response.",
    response_model=ChatResponse,
    response_description="LLM's response to the question."
)
@safe_call
async def ask_question(
        question: Optional[str] = "",
        model: Optional[str] = DEFAULT_MODEL
):
    return await ask_question_tool(question, model)


@router.get(
    "/classify",
    summary="Classify input text",
    description="Classifies the input text using a language model.",
    response_model=ChatResponse,
    response_description="Classification result."
)
@safe_call
async def classify(
        text: str = Query(..., min_length=1, description="Text to classify"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await classify_tool(text, model)


@router.get(
    "/sentiment",
    summary="Analyze sentiment",
    description="Analyzes the sentiment of the input text (e.g., positive, negative, neutral).",
    response_model=ChatResponse,
    response_description="Sentiment analysis result."
)
@safe_call
async def sentiment(
        text: str = Query(..., min_length=1, description="Text to analyze for sentiment"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await sentiment_tool(text, model)


@router.get(
    "/complete",
    summary="Complete text",
    description="Completes the given partial text using AI.",
    response_model=ChatResponse,
    response_description="The completed text."
)
@safe_call
async def complete_text(
        text: str = Query(..., min_length=1, description="Text to complete"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await complete_text_tool(text, model)


@router.get(
    "/generate-text",
    summary="Generate paragraph",
    description="Generates a paragraph of text on the given topic.",
    response_model=ChatResponse,
    response_description="Generated text paragraph."
)
@safe_call
async def generate_text(
        topic: str = Query(..., min_length=1, description="Topic to generate text about"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await generate_text_tool(topic, model)


@router.get(
    "/summarize",
    summary="Summarize text",
    description="Summarizes the input text.",
    response_model=ChatResponse,
    response_description="Summary of the input text."
)
@safe_call
async def summarize(
        text: str = Query(..., min_length=1, description="Text to summarize"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await summarize_tool(text, model)


@router.get(
    "/translate",
    summary="Translate text",
    description="Translates input text into the specified target language.",
    response_model=ChatResponse,
    response_description="Translated text."
)
@safe_call
async def translate(
        text: str = Query(..., min_length=1, description="Text to translate"),
        language: Optional[str] = Query("Spanish", min_length=1, description="Target language"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await translate_tool(text, language, model)


@router.get(
    "/paraphrase",
    summary="Paraphrase text",
    description="Paraphrases the input text in a formal tone.",
    response_model=ChatResponse,
    response_description="Paraphrased version of the input text."
)
@safe_call
async def paraphrase(
        text: str = Query(..., min_length=1, description="Text to paraphrase"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await paraphrase_tool(text, model)


@router.get(
    "/instruction",
    summary="Follow step-by-step instructions",
    description="Follows and executes instructions in a step-by-step manner.",
    response_model=ChatResponse,
    response_description="Response based on following the provided task instructions."
)
@safe_call
async def instruction(
        task: str = Query(..., min_length=1, description="Instructional task to perform"),
        model: Optional[str] = DEFAULT_MODEL
):
    return await instruction_tool(task, model)

