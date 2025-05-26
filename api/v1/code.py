import logging
from tools.code import *
from agents.code import code_mcp
from models.types import CodePrompt, CodeInput
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/code", tags=["Coding endpoints"])
logger = logging.getLogger(__name__)


def safe_call(fn):
    async def wrapper(*args, **kwargs):
        try:
            return {"result": await fn(*args, **kwargs)}
        except Exception as e:
            logger.exception(f"Code tool error in {fn.__name__}: {e}")
            raise HTTPException(status_code=500, detail="Code tool failed")
    return wrapper



@router.get("/")
async def get_coding_tools():
    response = await code_mcp.get_tools()
    return {"status": response.__str__()}

@router.post("/generate")
@safe_call
async def generate_code(payload: CodePrompt):
    try:
        return {"result": await generate_code_tool(prompt=payload.prompt, language=payload.language, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix")
@safe_call
async def fix_code(payload: CodeInput):
    try:
        return {"result": await fix_code_tool(code=payload.code, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
@safe_call
async def explain_code(payload: CodeInput):
    try:
        return {"result": await explain_code_tool(code=payload.code, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
@safe_call
async def write_tests(payload: CodeInput):
    try:
        return {"result": await write_tests_tool(code=payload.code, language=payload.language, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debug")
@safe_call
async def debug_code(payload: CodeInput):
    try:
        return {"result": await debug_code_tool(code=payload.code, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docstring")
@safe_call
async def generate_docstring(payload: CodeInput):
    try:
        return {"result": await generate_function_docstring_tool(code=payload.code, model=payload.model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
