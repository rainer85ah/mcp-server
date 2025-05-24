from typing import Optional
from pydantic import BaseModel


class ChatResponse(BaseModel):
    result: str


class CodePrompt(BaseModel):
    prompt: str
    language: Optional[str] = "python"
    model: Optional[str] = None


class CodeInput(BaseModel):
    code: str
    language: Optional[str] = "python"
    model: Optional[str] = None
