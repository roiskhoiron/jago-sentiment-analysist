import pandas as pd
import logging
from collections import Counter

logger = logging.getLogger(__name__)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess text data.

    Args:
        df: DataFrame with text columns

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    df['clean_text'] = df['content'].astype(str).fillna('').str.lower()
    texts = Counter(df['clean_text'])
    logger.info(f"Processed {len(df)} reviews with {len(texts)} unique texts")
    return df