import logging
from sklearn.metrics import classification_report

logger = logging.getLogger(__name__)

def evaluate(model, X, y, labels=None):
    """
    Evaluate model performance.

    Args:
        model: Trained model
        X: Feature matrix
        y: True labels
        labels: Label order

    Returns:
        Classification report dict
    """
    y_pred = model.predict(X)
    report = classification_report(y, y_pred, labels=labels, output_dict=True)
    logger.info(f"Accuracy: {report['accuracy']:.3f}")
    return report