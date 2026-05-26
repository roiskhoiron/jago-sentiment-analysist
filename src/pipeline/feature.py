import logging
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

def feature_engineering(df: pd.DataFrame, ngram_range=(1, 2)) -> tuple:
    """
    Create feature matrix using TF-IDF.

    Args:
        df: DataFrame with clean_text column
        ngram_range: Range of n-grams (default: (1,2))

    Returns:
        Features (X), labels (y), vectorizer
    """
    logger.info("Creating TF-IDF features")
    vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_features=10000)
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']
    logger.info(f"Features shape: {X.shape}")
    return X, y, vectorizer