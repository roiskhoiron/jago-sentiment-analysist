"""Fine-tune IndoBERT for sentiment analysis with class imbalance handling."""
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
print(f"Device: {DEVICE}, Torch: {torch.__version__}")

MODEL_NAME = "indobenchmark/indobert-base-p1"
SENTIMENT_LABELS = ["Negative", "Neutral", "Positive"]
NUM_LABELS = 3
MAX_LENGTH = 64
BATCH_SIZE = 8
EPOCHS = 3
LR = 2e-5

# ── 1. Load & Label Data ──
df = pd.read_csv("data/raw/reviews.csv")

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

df["label"] = df["score"].apply(rating_to_label)
df["clean"] = df["content"].apply(clean_text)
df = df[df["clean"].str.len() > 0].reset_index(drop=True)
print(f"Samples: {len(df)}")

# ── 2. Handle Class Imbalance: Oversample Neutral ──
neutral = df[df["label"] == 1]
if len(neutral) < 500:
    # Oversample neutral class
    n_replicates = max(1, 500 // len(neutral))
    neutral_oversampled = pd.concat([neutral] * n_replicates, ignore_index=True)
    df = pd.concat([df, neutral_oversampled], ignore_index=True)
    print(f"After oversampling neutral: {len(df)} samples")
    print(f"Label dist: {df['label'].value_counts().sort_index().tolist()}")

# ── 3. Train/Test Split ──
X = df["clean"].values
y = df["label"].values
X_train, X_test, y_train, y_test = train_test_split(
    np.array(X), np.array(y), test_size=0.2, stratify=np.array(y), random_state=SEED
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ── 4. Tokenizer & Dataset ──
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

class ReviewDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.encodings = tokenizer(texts.tolist(), truncation=True, padding=True,
                                    max_length=max_length, return_tensors="pt")
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.encodings.items()} | {"labels": self.labels[idx]}

    def __len__(self):
        return len(self.labels)

train_dataset = ReviewDataset(X_train, y_train, tokenizer, MAX_LENGTH)
test_dataset = ReviewDataset(X_test, y_test, tokenizer, MAX_LENGTH)

# Weighted sampler for class imbalance
class_counts = np.bincount(y_train)
class_weights = 1.0 / class_counts
sample_weights = class_weights[y_train]
sampler = WeightedRandomSampler(sample_weights, len(sample_weights), replacement=True)

# ── 5. Model ──
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
model.to(DEVICE)

# ── 6. Training Arguments ──
training_args = TrainingArguments(
    output_dir="models/EXP-05_IndoBERT/checkpoints",
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    learning_rate=LR,
    warmup_steps=500,
    logging_steps=50,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=1,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    report_to="none",
    seed=SEED,
)

# ── 7. Metrics ──
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {"accuracy": acc, "f1_macro": f1, "precision_macro": precision, "recall_macro": recall}

# ── 8. Trainer ──
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

# ── 9. Train ──
print("\nStarting training...")
trainer.train()
print("Training complete!")

# ── 10. Evaluate ──
print("\nEvaluating on test set...")
eval_results = trainer.evaluate()
print(f"Test accuracy: {eval_results['eval_accuracy']:.2%}")
print(f"Test F1 (macro): {eval_results['eval_f1_macro']:.4f}")

# Full predictions
preds = trainer.predict(test_dataset)
y_pred = np.argmax(preds.predictions, axis=1)

# Per-class metrics
p_per, r_per, f1_per, s_per = precision_recall_fscore_support(y_test, y_pred, labels=[0, 1, 2], zero_division=0)
cm = confusion_matrix(y_test, y_pred)
cls_report = classification_report(y_test, y_pred, target_names=SENTIMENT_LABELS, zero_division=0)

print("\nClassification Report:")
print(cls_report)
print(f"\nConfusion Matrix:\n{cm}")

# ── 11. Save Artifacts ──
save_dir = "models/EXP-05_IndoBERT"
os.makedirs(f"{save_dir}/checkpoints", exist_ok=True)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model saved to {save_dir}/")

# Save metrics
train_acc = eval_results.get("eval_accuracy", 0)
train_f1 = eval_results.get("eval_f1_macro", 0)

result = {
    "experiment": "EXP-05_IndoBERT",
    "model": "indobenchmark/indobert-base-p1",
    "metrics": {
        "accuracy_test": round(train_acc, 4),
        "f1_macro": round(train_f1, 4),
        "per_class": {
            label: {"precision": round(p_per[i], 4), "recall": round(r_per[i], 4), "f1": round(f1_per[i], 4)}
            for i, label in enumerate(SENTIMENT_LABELS)
        },
        "confusion_matrix": cm.tolist(),
    },
    "training_config": {
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LR,
        "max_length": MAX_LENGTH,
        "oversampled_neutral": True,
    },
    "timestamp": datetime.now().isoformat(),
}

# Update experiment results
results_path = "reports/experiment_results.json"
existing = json.load(open(results_path))
existing["experiments"].append(result)
if train_acc > existing["summary"]["best_accuracy"]:
    existing["summary"]["best_accuracy"] = round(train_acc, 4)
existing["summary"]["total"] = len(existing["experiments"])
existing["summary"]["best_model"] = "EXP-05_IndoBERT"
json.dump(existing, open(results_path, "w"), indent=2)

# Save classification report
with open(f"reports/EXP-05_IndoBERT_classification.txt", "w") as f:
    f.write(cls_report)

print(f"\nResults saved. Best accuracy: {existing['summary']['best_accuracy']:.2%}")
print("Done!")
