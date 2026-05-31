def format_history(history):
    return "\n".join([f"User: {pair[0]}\nSerenity: {pair[1]}" for pair in history[-5:]])


def detect_crisis(text):
    # Simple keyword-based detection for now
    crisis_keywords = ["kill myself", "suicidal", "can't go on", "end it all"]
    return any(kw in text.lower() for kw in crisis_keywords)
