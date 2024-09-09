import os
from langchain_anthropic import ChatAnthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", None)

anthropic_chat = ChatAnthropic(
    model_name='claude-3-opus-20240229',
    api_key=ANTHROPIC_API_KEY,
    temperature=0.5,
)
