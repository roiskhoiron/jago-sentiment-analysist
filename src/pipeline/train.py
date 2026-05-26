import logging
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

logger = logging.getLogger(__name__)

def train_model(X, y, model_path='models/baseline.pkl') -> LogisticRegression:
    """
    Train a basic classifier.

    Args:
        X: Feature matrix
        y: Labels
        model_path: Path to save model

    Returns:
        Trained model
    """
    logger.info("Training model")
    model = LogisticRegression(class_weight='balanced')
    model.fit(X, y)
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    return model