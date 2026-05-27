"""Continue tuning IndoBERT from checkpoint to target >92% accuracy."""
import os, json, re, warnings
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, WeightedRandomSampler
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments, set_seed,
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from datetime import datetime

warnings.filterwarnings("ignore")
SEED = 42
set_seed(SEED)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")

MODEL_PATH = "models/EXP-05_IndoBERT"
SENTIMENT_LABELS = ["Negative", "Neutral", "Positive"]
MAX_LENGTH = 96
BATCH_SIZE = 8
EXTRA_EPOCHS = 2
LR = 1e-5

# ── 1. Load Data ──
def rating_to_label(score):
    if score <= 2: return 0
    if score == 3: return 1
    return 2

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df = pd.read_csv("data/raw/reviews.csv")
df["label"] = df["score"].apply(rating_to_label)
df["clean"] = df["content"].apply(clean_text)
df = df[df["clean"].str.len() > 0].reset_index(drop=True)

# Oversample neutral
neutral = df[df["label"] == 1]
if len(neutral) < 500:
    n_replicates = max(1, 500 // len(neutral))
    df = pd.concat([df, pd.concat([neutral] * n_replicates, ignore_index=True)], ignore_index=True)

X = np.array(df["clean"].values)
y = np.array(df["label"].values)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ── 2. Tokenizer & Dataset ──
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

class ReviewDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=max_length, return_tensors="pt")
        self.encodings = encodings
        self.labels = torch.tensor(labels, dtype=torch.long)
    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.encodings.items()} | {"labels": self.labels[idx]}
    def __len__(self):
        return len(self.labels)

train_dataset = ReviewDataset(X_train, y_train, tokenizer, MAX_LENGTH)
test_dataset = ReviewDataset(X_test, y_test, tokenizer, MAX_LENGTH)

# ── 3. Load Model from Checkpoint ──
print("Loading model from checkpoint...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=3)
model.to(DEVICE)
print("Model loaded.")

# ── 4. Training Args ──
training_args = TrainingArguments(
    output_dir="models/EXP-05_IndoBERT/tuning",
    num_train_epochs=EXTRA_EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    learning_rate=LR,
    warmup_steps=200,
    logging_steps=50,
    eval_strategy="steps",
    eval_steps=200,
    save_strategy="steps",
    save_steps=200,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    report_to="none",
    seed=SEED,
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = accuracy_score(labels, preds)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {"accuracy": acc, "f1_macro": f1}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

# ── 5. Train ──
print(f"\nResuming training for {EXTRA_EPOCHS} epochs (LR={LR})...")
trainer.train()
print("Tuning complete!")

# ── 6. Evaluate ──
eval_results = trainer.evaluate()
print(f"\nTest accuracy: {eval_results['eval_accuracy']:.2%}")

preds = trainer.predict(test_dataset)
y_pred = np.argmax(preds.predictions, axis=1)
acc = accuracy_score(y_test, y_pred)

# Per-class
p_per, r_per, f1_per, s_per = precision_recall_fscore_support(y_test, y_pred, labels=[0, 1, 2], zero_division=0)
cm = confusion_matrix(y_test, y_pred)
cls_report = classification_report(y_test, y_pred, target_names=SENTIMENT_LABELS, zero_division=0)

print(cls_report)
print(f"Confusion Matrix:\n{cm}")
print(f"Accuracy: {acc:.2%}")

# ── 7. Save tuned model ──
tuned_dir = "models/EXP-06_IndoBERT_Tuned"
os.makedirs(tuned_dir, exist_ok=True)
model.save_pretrained(tuned_dir)
tokenizer.save_pretrained(tuned_dir)
print(f"Tuned model saved to {tuned_dir}/")

# ── 8. Save Results ──
result = {
    "experiment": "EXP-06_IndoBERT_Tuned",
    "model": "indobenchmark/indobert-base-p1 (tuned)",
    "metrics": {
        "accuracy_test": round(acc, 4),
        "f1_macro": round(eval_results['eval_f1_macro'], 4),
        "per_class": {
            label: {"precision": round(p_per[i], 4), "recall": round(r_per[i], 4), "f1": round(f1_per[i], 4)}
            for i, label in enumerate(SENTIMENT_LABELS)
        },
        "confusion_matrix": cm.tolist(),
    },
    "training_config": {
        "base_model": MODEL_PATH,
        "extra_epochs": EXTRA_EPOCHS,
        "learning_rate": LR,
        "max_length": MAX_LENGTH,
    },
    "timestamp": datetime.now().isoformat(),
}

results_path = "reports/experiment_results.json"
existing = json.load(open(results_path))
existing["experiments"].append(result)
if acc > existing["summary"]["best_accuracy"]:
    existing["summary"]["best_accuracy"] = round(acc, 4)
existing["summary"]["total"] = len(existing["experiments"])
existing["summary"]["best_model"] = f"EXP-06 ({acc:.2%})"
json.dump(existing, open(results_path, "w"), indent=2)

with open(f"reports/EXP-06_IndoBERT_Tuned_classification.txt", "w") as f:
    f.write(cls_report)

print(f"\nBest accuracy: {existing['summary']['best_accuracy']:.2%}")
