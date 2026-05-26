---
evaluation_protocol_version: 1.0.0
created: 2026-05-26T10:10:00Z
---

# Evaluation Protocol Definition

## Overview

Protokol evaluasi standar untuk semua eksperimen dalam proyek Sentiment Analysis Pipeline ulasan mobile banking Indonesia. Protokol ini memastikan konsistensi metrik, reproduktibilitas, dan validasi target akurasi >= 85%.

## 1. Train/Test Split Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Split Ratio | 80% train / 20% test | Standar untuk dataset 10k+ samples, memberikan cukup data training dan evaluasi |
| Stratification | stratify=y (label distribution) | Mempertahankan proporsi kelas (Positive/Neutral/Negative) di split |
| Random Seed | 42 | Deterministik — hasil dapat direproduksi di Colab, Jupyter, atau local |
| Shuffle | True (before split) | Menghindari bias berdasarkan urutan data |

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42,
    shuffle=True
)
```

## 2. Evaluation Metrics

### Primary Metric
- **Accuracy (Testing)** — Target: >= 85%
  - Metrik utama untuk menentukan apakah model memenuhi minimum requirement submission.

### Secondary Metrics
- **Precision per Class** — Minimum: >= 0.80 per kelas
  - Mengukur seberapa akurat prediksi positif untuk setiap sentimen.
- **Recall per Class** — Minimum: >= 0.80 per kelas
  - Mengukur seberapa baik model mendeteksi semua instances dari setiap kelas.
- **F1-Score (Macro)** — Minimum: >= 0.83
  - Rata-rata F1 tanpa weight berdasarkan class distribution.
- **F1-Score (Weighted)** — Minimum: >= 0.84
  - Rata-rata F1 dengan weight berdasarkan support per kelas.

### Confusion Matrix
- Dihasilkan untuk setiap eksperimen
- Format: 3x3 matrix (Positive, Neutral, Negative)
- Menampilkan distribusi kesalahan prediksi antar kelas
- Target: diagonal elements > off-diagonal elements

## 3. Evaluation Procedure

```
1. Load trained model + vectorizer/tokenizer
2. Predict on test set: y_pred = model.predict(X_test)
3. Compute metrics:
   - accuracy_score(y_test, y_pred)
   - precision_score(y_test, y_pred, average='macro')
   - recall_score(y_test, y_pred, average='macro')
   - f1_score(y_test, y_pred, average='macro')
   - classification_report(y_test, y_pred)  # per-class metrics
   - confusion_matrix(y_test, y_pred)
4. Validate against targets:
   - accuracy_testing >= 0.85 ✓
   - precision_per_class >= 0.80 ✓
   - recall_per_class >= 0.80 ✓
   - f1_macro >= 0.83 ✓
5. Check overfitting:
   - abs(train_accuracy - test_accuracy) <= 0.10 ✓
```

## 4. Overfitting Detection

| Criteria | Threshold | Method |
|----------|-----------|--------|
| Train vs Test Accuracy Gap | <= 10% | Compare train_acc and test_acc |
| Train vs Test F1 Gap | <= 10% | Compare train_f1_macro and test_f1_macro |
| Validation Curve | Flat or slightly declining | No sharp drop beyond training data |

```python
def check_overfitting(train_acc, test_acc):
    gap = abs(train_acc - test_acc)
    return gap <= 0.10, f"Gap: {gap:.2%}"
```

## 5. Label Encoding

| Raw Rating | Sentiment Label | Numeric Code |
|------------|-----------------|---------------|
| 1 | Negative | 0 |
| 2 | Negative | 0 |
| 3 | Neutral | 1 |
| 4 | Positive | 2 |
| 5 | Positive | 2 |

```python
def map_rating_to_sentiment(rating):
    if rating <= 2:
        return 'Negative'
    elif rating == 3:
        return 'Neutral'
    else:  # rating >= 4
        return 'Positive'
```

## 6. Reporting Format

Setiap eksperimen menghasilkan laporan evaluasi dengan format:

```yaml
evaluation_results:
  experiment_id: EXP-01
  model: LogisticRegression
  metrics:
    accuracy_test: 0.8723
    precision_macro: 0.8651
    recall_macro: 0.8645
    f1_macro: 0.8648
    f1_weighted: 0.8692
    per_class:
      Positive:
        precision: 0.8912
        recall: 0.8734
        f1: 0.8822
      Neutral:
        precision: 0.8234
        recall: 0.8456
        f1: 0.8344
      Negative:
        precision: 0.8567
        recall: 0.8389
        f1: 0.8477
    confusion_matrix: [[1234, 89, 45], [34, 567, 78], [23, 56, 1123]]
  overfitting_check:
    train_accuracy: 0.8945
    test_accuracy: 0.8723
    gap: 0.0222
    passed: true
  target_validation:
    accuracy_target_met: true
    precision_target_met: true
    recall_target_met: true
    f1_target_met: true
```

## 7. Cross-Validation Protocol

| Parameter | Value |
|-----------|-------|
| Method | K-Fold (k=5) |
| Shuffle | True |
| Stratified | True |
| Scoring | macro F1 |
| Report | mean +/- std across folds |

## 8. Artifact Storage

Setelah evaluasi, artifact disimpan di:

| Artifact | Location | Format |
|----------|----------|--------|
| Model | `models/{experiment_id}/model.{ext}` | .joblib (LR/SVM), .bin (IndoBERT) |
| Vectorizer | `models/vectorizers/{experiment_id}/vectorizer.{ext}` | .joblib / tokenizer checkpoint |
| Metrics Report | `reports/{experiment_id}_metrics.json` | JSON |
| Confusion Matrix | `reports/{experiment_id}_cm.png` | PNG visualization |
| Classification Report | `reports/{experiment_id}_class_report.txt` | Text |

## Dependencies

- **Experiment Matrix Design** (experiment-matrix-design) — sudah divalidasi ✅
- Preprocessing module dari dataset-strategy-validation
- Training pipeline dari ml-pipeline-architecture
