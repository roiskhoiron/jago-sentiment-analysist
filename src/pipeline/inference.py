import joblib
import logging
from typing import List, Union

logger = logging.getLogger(__name__)

def predict(text: str, model_path: str = "models/lr_model.pkl",
            vectorizer_path: str = "artifacts/tfidf_vectorizer.pkl") -> str:
    """
    Predict sentiment label for a single review text.

    Args:
        text: Input review text (Indonesian)
        model_path: Path to trained model file
        vectorizer_path: Path to TF-IDF vectorizer file

    Returns:
        Sentiment label: 'Positive', 'Neutral', or 'Negative'
    """
    logger.info(f"Predicting sentiment for text (length={len(text)})")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    features = vectorizer.transform([text])
    label = model.predict(features)[0]

    # Map numeric prediction to categorical label
    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiment = label_map.get(int(label), str(label))

    logger.info(f"Prediction: {sentiment}")
    return sentiment


def predict_batch(texts: List[str], model_path: str = "models/lr_model.pkl",
                  vectorizer_path: str = "artifacts/tfidf_vectorizer.pkl") -> List[str]:
    """
    Predict sentiment labels for a batch of review texts.

    Args:
        texts: List of input review texts (Indonesian)
        model_path: Path to trained model file
        vectorizer_path: Path to TF-IDF vectorizer file

    Returns:
        List of sentiment labels (Positive, Neutral, or Negative)
    """
    logger.info(f"Predicting sentiment for {len(texts)} texts")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    features = vectorizer.transform(texts)
    labels = model.predict(features)

    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiments = [label_map.get(int(l), str(l)) for l in labels]

    logger.info(f"Batch predictions complete: {len(sentiments)} items")
    return sentiments
