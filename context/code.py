from mcp.server.fastmcp import Context
from typing import Dict, List
from utils.logger_config import configure_logger

LAST_N_MESSAGES = 3
code_thread_store: Dict[str, List[Dict]] = {}  # Each message is a dict with role + content

logger = configure_logger("CodingContext")

def get_code_context(ctx: Context) -> List[Dict]:
    return code_thread_store.get(ctx.request_id, [])

def append_code_context(ctx: Context, new_turn: Dict):
    session_id = ctx.request_id
    code_thread_store.setdefault(session_id, []).append(new_turn)
    code_thread_store[session_id] = code_thread_store[session_id][-LAST_N_MESSAGES:]
    logger.info(f"[{session_id}] Memory updated with {len(code_thread_store[session_id])} turns.")

