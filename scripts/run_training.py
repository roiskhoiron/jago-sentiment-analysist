"""Training pipeline: load, label, preprocess, train 3 experiments, evaluate."""
import os, json, joblib, warnings, re, string
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             confusion_matrix, classification_report)
from nltk.corpus import stopwords
from tqdm import tqdm

warnings.filterwarnings("ignore")
SEED = 42
np.random.seed(SEED)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ── 1. Load Data ──
print("Loading data...")
df = pd.read_csv("data/raw/reviews.csv")

# ── 2. Label Mapping (Rating → Sentiment) ──
SENTIMENT_LABELS = ["Negative", "Neutral", "Positive"]

def rating_to_label(score):
    if score <= 2: return 0
    if score == 3: return 1
    return 2

df["label"] = df["score"].apply(rating_to_label)
print(f"Label distribution:\n{df['label'].value_counts().sort_index()}")
print(f"  → {', '.join(f'{SENTIMENT_LABELS[i]}: {c}' for i,c in df['label'].value_counts().sort_index().items())}")

# ── 3. Preprocessing ──
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

try:
    STOPWORDS = set(stopwords.words("indonesian"))
except:
    STOPWORDS = set()

print("Cleaning text...")
df["clean"] = df["content"].apply(clean_text)
# Filter out empty reviews
df = df[df["clean"].str.len() > 0].reset_index(drop=True)
print(f"After cleaning: {len(df)} samples")

# ── 4. Train/Test Split ──
X = df["clean"].values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=SEED, shuffle=True
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ── 5. Experiments ──
experiments = [
    {
        "id": "EXP-01_LR_TFIDF",
        "model_name": "LogisticRegression",
        "vectorizer_params": {"max_features": 10000, "ngram_range": (1, 2)},
        "model": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED, n_jobs=-1),
    },
    {
        "id": "EXP-02_SVM_TFIDF",
        "model_name": "LinearSVC",
        "vectorizer_params": {"max_features": 15000, "ngram_range": (1, 2)},
        "model": LinearSVC(max_iter=2000, class_weight="balanced", random_state=SEED),
    },
    {
        "id": "EXP-03_LR_BoW",
        "model_name": "LogisticRegression_BoW",
        "vectorizer_params": {"max_features": 8000, "ngram_range": (1, 1)},
        "model": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED, n_jobs=-1),
    },
]

results_list = []

for exp in tqdm(experiments, desc="Training experiments"):
    print(f"\n{'='*60}")
    print(f"Running {exp['id']}")

    # Vectorize
    vectorizer = TfidfVectorizer(**exp["vectorizer_params"], stop_words=None, sublinear_tf=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train
    model = exp["model"]
    model.fit(X_train_vec, y_train)

    # Predict
    y_pred = model.predict(X_test_vec)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Per-class metrics
    per_class = {}
    p_per, r_per, f1_per, s_per = precision_recall_fscore_support(y_test, y_pred, labels=[0, 1, 2], zero_division=0)
    for i, label in enumerate(SENTIMENT_LABELS):
        per_class[label] = {
            "precision": round(p_per[i], 4),
            "recall": round(r_per[i], 4),
            "f1": round(f1_per[i], 4),
            "support": int(s_per[i]),
        }

    result = {
        "experiment": exp["id"],
        "model": exp["model_name"],
        "vectorizer_params": exp["vectorizer_params"],
        "split": {"train": len(X_train), "test": len(X_test), "ratio": 0.2, "stratified": True},
        "metrics": {
            "accuracy": round(acc, 4),
            "precision_macro": round(precision, 4),
            "recall_macro": round(recall, 4),
            "f1_macro": round(f1, 4),
            "per_class": per_class,
            "confusion_matrix": cm,
        },
        "timestamp": datetime.now().isoformat(),
        "status": "completed",
    }
    results_list.append(result)

    # Save artifacts
    model_dir = f"models/{exp['id']}"
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, f"{model_dir}/model.pkl")
    joblib.dump(vectorizer, f"{model_dir}/vectorizer.pkl")

    cls_report = classification_report(y_test, y_pred, target_names=SENTIMENT_LABELS, zero_division=0)
    print(cls_report)
    print(f"Accuracy: {acc:.2%} | F1 (macro): {f1:.4f}")

    # Save per-class report
    with open(f"reports/{exp['id']}_classification.txt", "w") as f:
        f.write(cls_report)

# Save combined results
summary = {
    "experiments": results_list,
    "summary": {
        "total": len(results_list),
        "best_accuracy": max(r["metrics"]["accuracy"] for r in results_list),
        "best_f1": max(r["metrics"]["f1_macro"] for r in results_list),
        "timestamp": datetime.now().isoformat(),
    },
}

with open("reports/experiment_results.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n{'='*60}")
print("ALL EXPERIMENTS COMPLETE")
print(f"{'='*60}")
for r in results_list:
    marker = "★ BEST" if r["metrics"]["accuracy"] == summary["summary"]["best_accuracy"] else ""
    print(f"  {r['experiment']}: acc={r['metrics']['accuracy']:.2%}  f1={r['metrics']['f1_macro']:.4f}  {marker}")
print(f"\nResults saved to reports/experiment_results.json")
