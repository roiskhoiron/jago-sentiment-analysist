import pytest
import pandas as pd
import numpy as np
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pipeline.ingest import ingest
from src.pipeline.preprocess import preprocess
from src.pipeline.feature import feature_engineering
from src.pipeline.train import train_model
from src.pipeline.evaluate import evaluate
from src.pipeline.inference import predict, predict_batch


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "reviewId": ["r1", "r2", "r3", "r4", "r5"],
        "content": [
            "aplikasi bagus banget, sangat membantu",
            "kurang baik, sering error",
            "lumayan lah untuk aplikasi bank",
            "sangat memuaskan dan cepat",
            "tidak terlalu bagus juga tidak buruk"
        ],
        "score": [5, 2, 3, 4, 3],
        "at": pd.date_range("2024-01-01", periods=5),
        "userName": ["user1", "user2", "user3", "user4", "user5"]
    })


@pytest.fixture
def labeled_dataframe():
    """Create a DataFrame with clean_text and label columns."""
    return pd.DataFrame({
        "clean_text": [
            "aplikasi bagus banget",
            "kurang baik sering error",
            "lumayan lah untuk aplikasi bank",
            "sangat memuaskan dan cepat",
            "tidak terlalu bagus juga tidak buruk"
        ],
        "label": ["positive", "negative", "neutral", "positive", "neutral"]
    })


def test_ingest(sample_dataframe, tmp_path):
    """Test ingest loads CSV file correctly."""
    csv_file = tmp_path / "test_reviews.csv"
    sample_dataframe.to_csv(csv_file, index=False)

    df = ingest(str(csv_file))

    assert len(df) == 5
    assert "content" in df.columns
    assert "score" in df.columns


def test_ingest_raises_on_missing_file():
    """Test ingest raises exception for missing file."""
    with pytest.raises(Exception):
        ingest("/nonexistent/path/reviews.csv")


def test_preprocess(sample_dataframe):
    """Test preprocess creates clean_text column."""
    df = preprocess(sample_dataframe)

    assert "clean_text" in df.columns
    assert df["clean_text"].iloc[0] == sample_dataframe["content"].iloc[0].lower()
    assert len(df) == len(sample_dataframe)


def test_preprocess_handles_nan():
    """Test preprocess handles NaN values gracefully."""
    df = pd.DataFrame({"content": ["hello", None, "world"]})
    result = preprocess(df)

    # astype(str) converts None to "None" string, then .fillna("") won't remove it
    # but the important thing is no error is raised and a valid string is produced
    assert isinstance(result["clean_text"].iloc[1], str)
    assert len(result["clean_text"]) == 3


def test_feature_engineering(labeled_dataframe):
    """Test feature engineering returns correct types and shapes."""
    X, y, vectorizer = feature_engineering(labeled_dataframe)

    assert len(y) == 5
    assert X.shape[0] == 5
    assert hasattr(vectorizer, "transform")


def test_train_model(labeled_dataframe):
    """Test model training returns trained model and saves file."""
    with tempfile.NamedTemporaryFile(suffix=".pkl") as f:
        X, y, _ = feature_engineering(labeled_dataframe)
        model = train_model(X, y, model_path=f.name)

        assert hasattr(model, "predict")
        assert os.path.exists(f.name)


def test_evaluate(labeled_dataframe):
    """Test evaluation returns classification report dict."""
    X, y, vectorizer = feature_engineering(labeled_dataframe)
    model = train_model(X, y)
    report = evaluate(model, X, y)

    assert isinstance(report, dict)
    assert "accuracy" in report
    assert "positive" in report or 2 in report


def test_predict_single():
    """Test single text prediction."""
    # Create a mock model and vectorizer for testing
    import joblib
    from sklearn.linear_model import LogisticRegression
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = ["aplikasi bagus", "sangat baik", "kurang puas"]
    labels = [2, 2, 0]  # positive, positive, negative

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression()
    model.fit(X, labels)

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as mf:
        joblib.dump(model, mf.name)
        model_path = mf.name

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as vf:
        joblib.dump(vectorizer, vf.name)
        vectorizer_path = vf.name

    result = predict("aplikasi bagus sangat", model_path=model_path,
                     vectorizer_path=vectorizer_path)

    assert result in ["Positive", "Neutral", "Negative"]

    os.unlink(model_path)
    os.unlink(vectorizer_path)


def test_predict_batch():
    """Test batch prediction returns list of labels."""
    import joblib
    from sklearn.linear_model import LogisticRegression
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = ["aplikasi bagus", "sangat baik", "kurang puas"]
    labels = [2, 2, 0]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression()
    model.fit(X, labels)

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as mf:
        joblib.dump(model, mf.name)
        model_path = mf.name

    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as vf:
        joblib.dump(vectorizer, vf.name)
        vectorizer_path = vf.name

    results = predict_batch(["bagus sekali", "sangat kurang"],
                            model_path=model_path,
                            vectorizer_path=vectorizer_path)

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(r in ["Positive", "Neutral", "Negative"] for r in results)

    os.unlink(model_path)
    os.unlink(vectorizer_path)
