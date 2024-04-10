# send_to_claude.py
import requests
from IPython.display import Markdown, display
from anthropic import HUMAN_PROMPT, AI_PROMPT
import base64
import asyncio


async def send_image_to_claude_api(image_content, media_type, client):
    # Read the local image file
    image_encode_1 = base64.b64encode(image_content).decode("utf-8")

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system="You are an AI assistant that analyzes images and describes the expression and emotional state of the person in the image.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_encode_1,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Give one line to describe only expression and emotional state of person in the image"
                    }
                ],
            }
        ],
    )
    return message.content[0].text
