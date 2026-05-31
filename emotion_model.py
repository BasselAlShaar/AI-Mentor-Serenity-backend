from transformers import pipeline

# Load pre-trained Hugging Face emotion model
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
)


def detect_emotion(text):
    emotions = emotion_pipeline(text)[0]
    top_emotion = max(emotions, key=lambda x: x["score"])
    return top_emotion["label"], top_emotion["score"]
