import pandas as pd
import logging

logger = logging.getLogger(__name__)

def ingest(filepath: str) -> pd.DataFrame:
    """
    Load raw review data from CSV.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with review data
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} reviews from {filepath}")
        return df
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        raise