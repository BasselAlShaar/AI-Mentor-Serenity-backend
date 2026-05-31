print("🔥 APP.PY IS RUNNING")

import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from gpt_engine import generate_response
from utils import detect_crisis

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory chat history
chat_history = {}


@app.route("/")
def home():
    return "Server is running"


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json(silent=True) or {}

        user_id = data.get("user_id", "default")
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400

        history = chat_history.get(user_id, [])

        # Crisis detection
        if detect_crisis(message):
            return jsonify({
                "response": "You're not alone 💙 Please reach out to someone you trust and seek immediate support.",
                "emotion": "concern",
                "crisis": True
            })

        try:
            # generate_response must return:
            # (ai_response, emotion)
            ai_response, emotion = generate_response(
                message,
                history
            )

        except Exception as e:
            print("GPT ERROR:")
            print(e)

            return jsonify({
                "response": "I'm having trouble responding right now 💔",
                "emotion": "neutral",
                "crisis": False
            }), 500

        # Save conversation
        history.append((message, ai_response))

        # Keep only latest 20 exchanges
        chat_history[user_id] = history[-20:]

        return jsonify({
            "response": ai_response,
            "emotion": emotion,
            "crisis": False
        })

    except Exception:
        print(traceback.format_exc())

        return jsonify({
            "error": "Internal Server Error"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)