print("🔥 APP.PY IS RUNNING")

import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from emotion_model import detect_emotion
from gpt_engine import generate_response
from utils import detect_crisis

app = Flask(__name__)

# ✅ ONLY ONE CORS CONFIG
CORS(app, resources={r"/*": {"origins": "*"}})

chat_history = {}


@app.route("/")
def home():
    return "Server is running"

@app.route("/chat", methods=["GET", "POST", "OPTIONS"])
def chat():

    # ✅ ALWAYS handle preflight FIRST
    if request.method == "OPTIONS":
        return "", 200

    try:
        # ✅ safe JSON parsing
        data = request.get_json(silent=True) or {}

        user_id = data.get("user_id", "default")
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Empty message"}), 400

        history = chat_history.get(user_id, [])

        # 🔥 wrap risky functions (VERY IMPORTANT)
        try:
            emotion, score = detect_emotion(message)
        except Exception as e:
            print("Emotion model error:", e)
            emotion, score = "neutral", 0.0

        if detect_crisis(message):
            return jsonify({
                "response": "You're not alone 💙 please reach out for support.",
                "emotion": emotion,
                "crisis": True
            })

        # 🔥 GPT call safety
        try:
            ai_response = generate_response(message, emotion, history)
        except Exception as e:
            print("GPT error:", e)
            return jsonify({
                "response": "I'm having trouble responding right now 💔",
                "emotion": emotion,
                "crisis": False
            }), 500

        history.append((message, ai_response))
        chat_history[user_id] = history[-20:]

        return jsonify({
            "response": ai_response,
            "emotion": emotion,
            "crisis": False
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)