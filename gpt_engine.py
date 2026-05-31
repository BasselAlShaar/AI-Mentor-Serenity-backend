from openai import OpenAI
from utils import format_history
import os

client = OpenAI(api_key=os.getenv("API_KEY"))  # ⚠️ keep this in env variable in production


def generate_response(user_input, emotion_label, history=None):
    if history is None:
        history = []

    # keep only last 6 messages to control cost
    history = history[-6:]

    prompt = f"""
You are Serenity, a kind, empathetic mental health companion AI.

The user feels {emotion_label.lower()}.

Recent conversation:
{format_history(history)}

User says: "{user_input}"

Respond in a warm, supportive, and compassionate tone.
Do not be robotic. Keep it natural and comforting.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Serenity, a warm, empathetic AI companion. "
                    "You provide emotional support in a natural conversational way."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.85,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()