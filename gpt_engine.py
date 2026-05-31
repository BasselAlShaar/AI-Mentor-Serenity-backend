from openai import OpenAI
from utils import format_history
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_emotion(text):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the user's emotion. "
                    "Return ONLY one word from this list:\n"
                    "joy, sadness, anger, fear, surprise, neutral"
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_completion_tokens=5
    )

    emotion = response.choices[0].message.content.strip().lower()

    allowed = {
        "joy",
        "sadness",
        "anger",
        "fear",
        "surprise",
        "neutral"
    }

    return emotion if emotion in allowed else "neutral"


def generate_response(user_input, history=None):

    if history is None:
        history = []

    history = history[-6:]

    emotion = detect_emotion(user_input)

    prompt = f"""
You are Serenity, a kind and empathetic emotional support companion.

Detected emotion: {emotion}

Recent conversation:
{format_history(history)}

User says:
{user_input}

Respond warmly, naturally, and conversationally.
Keep responses under 150 words.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Serenity, a warm, supportive AI companion. "
                    "Be empathetic, encouraging, and conversational."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=200
    )

    return (
        response.choices[0].message.content.strip(),
        emotion
    )