# send_to_claude.py
import requests
from IPython.display import Markdown, display
from anthropic import HUMAN_PROMPT, AI_PROMPT

def send_text_to_claude_api(text, system, client):
    message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system=system,
    messages=[{"role": "user", "content": text}]
    )
    return message
