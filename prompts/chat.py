from context.chat import get_chat_context
from agents.chat import chat_mcp
from mcp.server.fastmcp import Context
from typing import List, Dict


def format_prompt(system: str, user: str, history: List[Dict]) -> List[Dict]:
    return [
        {"role": "system", "content": system},
        *history,
        {"role": "user", "content": user}
    ]

@chat_mcp.prompt("ask_question", description="Prompt to answer natural language questions with memory context.")
def prompt_ask_question(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("You are a helpful assistant. Answer questions clearly and concisely.", input, history)

@chat_mcp.prompt("classify", description="Prompt to classify input text into a single appropriate category.")
def prompt_classify(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Classify the input text into a single best-fit category.", input, history)

@chat_mcp.prompt("sentiment", description="Prompt to return sentiment as Positive, Neutral, or Negative.")
def prompt_sentiment(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Analyze the text and return: Positive, Neutral, or Negative.", input, history)

@chat_mcp.prompt("summarize", description="Prompt to summarize user input into a concise paragraph.")
def prompt_summarize(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Summarize the user's input into a concise paragraph.", input, history)

@chat_mcp.prompt("complete_text", description="Prompt to continue partial input in a coherent and natural way.")
def prompt_complete_text(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Complete the following text in a coherent and natural way.", input, history)

@chat_mcp.prompt("generate_text", description="Prompt to write a well-structured and original paragraph on a topic.")
def prompt_generate_text(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Write a well-structured and original paragraph on this topic.", input, history)

@chat_mcp.prompt("translate", description="Prompt to translate text to a target language.")
def prompt_translate(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Translate the following text to the specified language.", input, history)

@chat_mcp.prompt("paraphrase", description="Prompt to paraphrase text in a more formal or professional tone.")
def prompt_paraphrase(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Rephrase this text to sound more professional and formal.", input, history)

@chat_mcp.prompt("instruction", description="Prompt to provide step-by-step instructions for a task.")
def prompt_instruction(input: str, ctx: Context):
    history = get_chat_context(ctx)
    return format_prompt("Provide step-by-step instructions for the following task.", input, history)
