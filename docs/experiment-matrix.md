---
work_item: experiment-matrix-design
created: 2026-05-26T10:00:00Z
---

# Experiment Matrix Design

## Overview

Matriks eksperimen untuk proyek Sentiment Analysis Pipeline pada ulasan mobile banking Indonesia. Mengcover minimal 3 variasi model dengan kombinasi ekstraksi fitur yang berbeda.

## Experiment Configuration Table

| # | Model | Feature Extraction | Vectorizer/Tokenizer | Split Config | Target Accuracy | Target F1 | K-Cross Validation |
|---|-------|-------------------|---------------------|--------------|-----------------|-----------|-------------------|
| EXP-01 | Logistic Regression | TF-IDF | TF-IDFVectorizer (max_features=10000, ngram_range=(1,2)) | train/test = 80/20 | >= 85% | >= 0.83 | 5-fold |
| EXP-02 | Linear SVM | TF-IDF | TF-IDFVectorizer (max_features=15000, ngram_range=(1,2)) | train/test = 80/20 | >= 87% | >= 0.86 | 5-fold |
| EXP-03 | IndoBERT (Fine-tuning) | Pre-trained IndoBERT embeddings | IndobertaPreprocessor (max_length=128) | train/test = 80/20 | >= 90% | >= 0.89 | 5-fold |
| EXP-04 | Logistic Regression | Bag-of-Words + Stopword Removal (Indonesian) | CountVectorizer (max_features=8000) | train/test = 75/25 | >= 84% | >= 0.82 | 5-fold |
| EXP-05 | Linear SVM | TF-IDF + Stemming (Sastrawi) | TF-IDFVectorizer (max_features=12000, ngram_range=(1,3)) | train/test = 80/20 | >= 88% | >= 0.87 | 5-fold |

## Feature Extraction Combinations

| Combination | Description | Applied To |
|-------------|-------------|------------|
| TF-IDF Standard | TF-IDF dengan bigram, max_features=10000 | EXP-01, EXP-03 |
| TF-IDF Extended | TF-IDF dengan trigram, max_features=15000 | EXP-02 |
| BoW + Stopword | CountVectorizer + Indonesian stopword removal (Sastrawi) | EXP-04 |
| TF-IDF + Stemming | TF-IDF setelah stemming Sastrawi, max_features=12000 | EXP-05 |

## Model Selection Criteria

| Criteria | Threshold | Rationale |
|----------|-----------|-----------|
| Accuracy (Testing) | >= 85% | Minimum requirement untuk submission |
| F1-Score (Macro) | >= 0.83 | Mencerminkan keseimbangan antar kelas 3 label |
| Precision (Per-Class) | >= 0.80 per kelas | Mencegah bias ke salah satu sentimen |
| Recall (Per-Class) | >= 0.80 per kelas | Minimal missed detection |
| Train vs Test Gap | <= 10% difference | Overfitting check |

## Preprocessing Pipeline

```
text_input → URL/emoji removal → Indonesian stopword removal (Sastrawi) → 
             optional stemming (Sastrawi) → tokenization → 
             feature extraction (TF-IDF / BoW / IndoBERT) → model inference
```

## Reproducibility

- Semua eksperimen menggunakan `random_state=42` dan `stratify=y` pada train/test split
- Seed untuk IndoBERT: `transformers.set_seed(42)`
- Artifact disimpan: model (.joblib / .bin), vectorizer/tokenizer, preprocessing config
- Config eksperimental disimpan dalam YAML di `docs/experiment-config.yaml`

## Dependencies

- **ML Pipeline Architecture** (ml-pipeline-architecture) — sudah divalidasi ✅
- Preprocessing module dari dataset-strategy-validation
- Labeling mapping: rating 1-2 → Negative, 3 → Neutral, 4-5 → Positive
