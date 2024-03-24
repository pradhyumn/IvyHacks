# send_to_claude.py
import requests
from IPython.display import Markdown, display
from anthropic import HUMAN_PROMPT, AI_PROMPT


def send_text_to_claude_api(text, api_key, client):
    message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system="Summarize the following resume making sure all the technical details are covered and concise",
    messages=[{"role": "user", "content": text}]
    )
    return message
