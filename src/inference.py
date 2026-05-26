"""Inference script: predict sentiment from text input."""
import os, re, joblib, sys
import numpy as np

SEED = 42
np.random.seed(SEED)
SENTIMENT_MAP = {0: "Negative", 1: "Neutral", 2: "Positive"}
MODEL_DIR = "models/EXP-02_SVM_TFIDF"

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

class SentimentAnalyzer:
    def __init__(self, model_dir=MODEL_DIR):
        self.model = joblib.load(f"{model_dir}/model.pkl")
        self.vectorizer = joblib.load(f"{model_dir}/vectorizer.pkl")

    def predict(self, text):
        clean = clean_text(text)
        vec = self.vectorizer.transform([clean])
        pred = self.model.predict(vec)[0]
        return SENTIMENT_MAP[pred]

    def predict_batch(self, texts):
        return [self.predict(t) for t in texts]

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = analyzer.predict(text)
        print(f"Sentimen: {result}")
    else:
        samples = [
            "aplikasi sangat membantu transaksi sehari-hari",
            "aplikasi sering error dan lambat",
            "aplikasi standar kadang lancar kadang lemot",
        ]
        for s in samples:
            print(f"Input: {s} -> Sentimen: {analyzer.predict(s)}")
