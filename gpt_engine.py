from openai import OpenAI
from utils import format_history
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is missing from environment variables")

client = OpenAI(api_key=api_key)

def detect_emotion(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        model="gpt-4o-mini",
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