import logging
from tools.chat import *
from typing import Optional
from models.types import ChatResponse
from fastapi import APIRouter, HTTPException, Query


router = APIRouter(prefix="/chat", tags=["Chat endpoints"])
logger = logging.getLogger(__name__)


def safe_call(fn):
    async def wrapper(*args, **kwargs):
        try:
            return {"result": await fn(*args, **kwargs)}
        except Exception as e:
            logger.exception(f"Chat tool error in {fn.__name__}: {e}")
            raise HTTPException(status_code=500, detail="Chat tool failed")
    return wrapper


@router.get("/ask", response_model=ChatResponse, summary="Ask LLM a question")
@safe_call
async def ask_question(question: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await ask_question_tool(question, model)


@router.get("/classify", response_model=ChatResponse, summary="Classify input text")
@safe_call
async def classify(text: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await classify_tool(text, model)


@router.get("/sentiment", response_model=ChatResponse, summary="Analyze text sentiment")
@safe_call
async def sentiment(text: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await sentiment_tool(text, model)


@router.get("/complete", response_model=ChatResponse, summary="Complete text")
@safe_call
async def complete_text(text: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await complete_text_tool(text, model)


@router.get("/generate-text", response_model=ChatResponse, summary="Generate a paragraph on a topic")
@safe_call
async def generate_text(topic: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await generate_text_tool(topic, model)


@router.get("/summarize", response_model=ChatResponse, summary="Summarize text")
@safe_call
async def summarize(text: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await summarize_tool(text, model)


@router.get("/translate", response_model=ChatResponse, summary="Translate text to a target language")
@safe_call
async def translate(
        text: str = Query(..., min_length=1),
        language: Optional[str] = Query("Spanish", min_length=1),
        model: Optional[str] = DEFAULT_MODEL
):
    return await translate_tool(text, language, model)


@router.get("/paraphrase", response_model=ChatResponse, summary="Paraphrase text formally")
@safe_call
async def paraphrase(text: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await paraphrase_tool(text, model)


@router.get("/instruction", response_model=ChatResponse, summary="Follow instructions step-by-step")
@safe_call
async def instruction(task: str = Query(..., min_length=1), model: Optional[str] = DEFAULT_MODEL):
    return await instruction_tool(task, model)
