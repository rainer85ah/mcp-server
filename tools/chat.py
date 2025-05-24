import datetime
from agents.chat import chat_agent


@chat_agent.tool()
def greet_user(name: str) -> str:
    """Greet the user based on current time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        part_of_day = "morning"
    elif hour < 18:
        part_of_day = "afternoon"
    else:
        part_of_day = "evening"
    return f"Good {part_of_day}, {name}! How can I help you today?"


@chat_agent.tool()
def summarize_conversation(conversation: list[str]) -> str:
    """Summarize a list of conversation messages into a brief paragraph."""
    if not conversation:
        return "The conversation is currently empty."
    summary = " ".join(conversation[-5:])  # simple last-5-messages summary
    return f"Summary of recent conversation: {summary}"


@chat_agent.tool()
def get_current_time() -> str:
    """Return the current system time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
