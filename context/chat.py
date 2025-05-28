from mcp.server.fastmcp import Context
from typing import List, Dict
from utils.logger_config import configure_logger

LAST_N_MESSAGES = 2
chat_memory_store: Dict[str, List[Dict]] = {}

logger = configure_logger("ChatContext")

def get_chat_context(ctx: Context) -> List[Dict]:
    return chat_memory_store.get(ctx.request_id, [])

def update_chat_context(ctx: Context, new_turn: Dict):
    session_id = ctx.request_id
    chat_memory_store.setdefault(session_id, []).append(new_turn)
    chat_memory_store[session_id] = chat_memory_store[session_id][-LAST_N_MESSAGES:]
    logger.info(f"[{session_id}] Memory updated with {len(chat_memory_store[session_id])} turns.")
