---
id: ml-pipeline-architecture
title: ML Pipeline Architecture - Documentation
type: architecture-doc
created: 2026-05-26T10:00:00Z
work_item_id: ml-pipeline-architecture
---

# ML Pipeline Architecture — Sentiment Analysis for Indonesian Reviews

## Data Flow Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    SENTIMENT ANALYSIS PIPELINE                      │
│                     (Indonesian Mobile Banking Reviews)             │
└─────────────────────────────────────────────────────────────────────┘

   ┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
   │  SCRAPING    │─────▶│  INGESTION   │─────▶│  PREPROCESSING   │
   │ (Google Play)│      │ (CSV Load)   │      │  (Clean & Normalize)│
   └──────────────┘      └──────────────┘      └────────┬─────────┘
        │                        │                      │
        │ reviews.csv            │ raw_df               │ clean_df
        │ (~10,000 rows)         │ (reviewId,           │ (clean_text,
        │                          content,             │  label)
        │                          score,               │
        │                          timestamp,           │
        │                          userName)             │
                                                        │
                                                ┌───────▼──────────┐
                                                │ FEATURE EXTRACTION│
                                                │ (TF-IDF / BERT)   │
                                                └───────┬──────────┘
                                                        │ X, y
                                                        │ (feature matrix,
                                                        │  label array)
                                                        │
                                   ┌────────────────────┼────────────────────┐
                                   │                    │                     │
                           ┌───────▼──────────┐  ┌──────▼──────────┐  ┌──────▼──────────┐
                           │   EXPERIMENT A   │  │ EXPERIMENT B    │  │ EXPERIMENT C    │
                           │ (TF-IDF + LR)    │  │ (TF-IDF + SVM)  │  │ (Fine-tune      │
                           │                  │  │                 │  │  IndoBERT)      │
                           └───────┬──────────┘  └──────┬──────────┘  └──────┬──────────┘
                                   │                    │                      │
                                   │ model.pkl          │ model.pkl            │ model_bert.bin
                                   │ (LR weights)       │ (SVM weights)        │ (BERT checkpoint)
                                   │                    │                      │
                           ┌───────▼──────────┐  ┌──────▼──────────┐  ┌──────▼──────────┐
                           │  EVALUATION      │  │  EVALUATION     │  │  EVALUATION     │
                           │                  │  │                 │  │                 │
                           │ • Accuracy        │  │ • Accuracy      │  │ • Accuracy      │
                           │ • Precision/Recall│  │ • Precision/    │  │ • Precision/    │
                           │ • F1 Score        │  │   Recall/F1     │  │   Recall/F1     │
                           │ • Confusion Matrix│  │ • Confusion     │  │ • Confusion     │
                           └──────────────────┘  │   Matrix        │  │   Matrix        │
                                                  └──────────────────┘  └──────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   INFERENCE     │
                                               │ (Predict Sentiment)│
                                               └─────────────────┘
                                                         │
                                                 Positive / Neutral /
                                                  Negative
```

## Component Input/Output Definitions

### 1. Scraping (`scripts/scrape_reviews.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Fetch real reviews from Google Play Store for Bank Jago |
| **Source** | Google Play Store API (google-play-scraper) |
| **Input** | `APP_ID=com.jago.android`, `LANG=id`, `COUNTRY=id` |
| **Output** | `data/raw/reviews.csv` — raw reviews in CSV format |
| **Output Schema** | `reviewId` (str), `content` (str), `score` (int 1-5), `at` (datetime), `userName` (str) |
| **Volume** | Target ≥ 10,000 unique reviews |
| **Rate Limiting** | 1000ms sleep between requests |

### 2. Ingestion (`src/pipeline/ingest.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Load raw review data from disk into DataFrame |
| **Input** | `filepath: str` — path to CSV file (e.g., `data/raw/reviews.csv`) |
| **Output** | `pd.DataFrame` — raw review DataFrame with columns: reviewId, content, score, at, userName |
| **Error Handling** | Raises exception if file not found or malformed |

### 3. Preprocessing (`src/pipeline/preprocess.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Clean text data and assign sentiment labels |
| **Input** | `pd.DataFrame` — raw review DataFrame from ingestion |
| **Processing** | 1. Fill NaN values with empty string<br>2. Convert to lowercase<br>3. URL/emoji removal (via emoji lib)<br>4. Indonesian stopword removal<br>5. Rating-to-label mapping: score 1-2 → `negative`, 3 → `neutral`, 4-5 → `positive` |
| **Output** | `pd.DataFrame` — cleaned DataFrame with new columns: `clean_text` (str), `label` (str) |
| **Label Distribution** | Expected balanced distribution across 3 classes |

### 4. Feature Extraction (`src/pipeline/feature.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Convert text data into numerical feature matrices for ML models |
| **Input** | `pd.DataFrame` with `clean_text` and `label` columns; optional `ngram_range=(1, 2)` |
| **Output** | Tuple `(X: sparse matrix, y: pd.Series, vectorizer: TfidfVectorizer)` for classical ML<br>OR<br>`datasets.Dataset` object for transformer fine-tuning (IndoBERT) |
| **Parameters** | TF-IDF: `max_features=10000`, `ngram_range=(1,2)`<br>BERT: tokenizer from `indobenchmark/indobert-base-p1` |

### 5. Training (`src/pipeline/train.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Train and persist classification models |
| **Input** | `X` (feature matrix), `y` (labels), optional `model_path: str`, `random_seed: int=42` |
| **Models** | 1. Logistic Regression (TF-IDF features)<br>2. Linear SVM (TF-IDF features)<br>3. IndoBERT (fine-tuned via Hugging Face Trainer) |
| **Output** | Trained model object saved to `models/` directory:<br>- `models/lr_model.pkl` — Logistic Regression<br>- `models/svm_model.pkl` — Linear SVM<br>- `models/bert_model/` — IndoBERT checkpoint + config.json + tokenizer |
| **Split Config** | 80% train / 20% test, stratified by label, fixed seed=42 |

### 6. Evaluation (`src/pipeline/evaluate.py`)

| Property | Description |
|----------|-------------|
| **Purpose** | Compute metrics and compare model performance |
| **Input** | `model: trained_model`, `X: feature_matrix`, `y: true_labels`, optional `labels=["negative", "neutral", "positive"]` |
| **Output** | Dict containing per-class precision, recall, F1, support + overall accuracy<br>+ Confusion matrix (np.ndarray or seaborn visualization) |
| **Metrics Reported** | Accuracy, Precision (macro/weighted), Recall (macro/weighted), F1-score, Confusion Matrix |
| **Success Threshold** | Testing accuracy ≥ 85%, at least one experiment with >92% train & test |

### 7. Inference (`src/pipeline/inference.py` — to be created)

| Property | Description |
|----------|-------------|
| **Purpose** | Predict sentiment label for new review text |
| **Input** | `text: str` (single review) or `texts: List[str]` (batch), optional `model_type: str = "lr"` |
| **Output** | `label: str` — categorial prediction: `Positive`, `Neutral`, or `Negative`<br>OR<br>`predictions: List[str]` for batch inference |
| **Model Loading** | Loads vectorizer/tokenizer + model from `models/` directory |

## Dependency Graph

```text
scrape_reviews.py
    │
    ▼
data/raw/reviews.csv
    │
    ▼
ingest() ──▶ preprocess() ──▶ feature_engineering()
                       │                     │
                       ▼                     ▼
                   clean_df          X (features), y (labels)
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
            LR Model              SVM Model          IndoBERT
            models/lr.pkl       models/svm.pkl     models/bert_model/
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       ▼
                                evaluate()
                                       │
                                       ▼
                              metrics.json + confusion matrix
                                       │
                                       ▼
                                inference.predict()
```

## Artifact Persistence

All pipeline artifacts are saved for reproducibility:

| Artifact | Path | Description |
|----------|------|-------------|
| Raw data | `data/raw/reviews.csv` | Scraped reviews from Google Play |
| Processed data | `data/processed/cleaned.csv` | Preprocessed + labeled data |
| LR model | `models/lr_model.pkl` | Trained Logistic Regression |
| SVM model | `models/svm_model.pkl` | Trained Linear SVM |
| BERT model | `models/bert_model/` | Fine-tuned IndoBERT checkpoint |
| TF-IDF vectorizer | `artifacts/tfidf_vectorizer.pkl` | Fitted TF-IDF vectorizer |
| BERT tokenizer | `artifacts/bert_tokenizer.json` | IndoBERT tokenizer config |
| Metrics | `reports/metrics.json` | Per-experiment metrics summary |
| Confusion matrices | `reports/confusion_matrices/` | Per-experiment visualization |

## Reproducibility Guarantees

| Factor | Approach |
|--------|----------|
| Random seeds | All operations use `RANDOM_SEED=42` (configurable) |
| Data split | Stratified split with fixed seed |
| Model artifacts | Saved after training, loaded for inference |
| Notebooks | Sequential execution (01 → 02 → 03), no manual modification needed |
| Dependencies | `requirements.txt` pins all packages |

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Modular Python functions over notebook-only code | Enables reproducibility in any environment (Colab, local, CI) |
| TF-IDF + LR/SVM as baselines first | Fast to train, establish benchmark for IndoBERT comparison |
| Rating-based labeling initially | Consistent, no manual annotation needed; verified via labeling strategy |
| Artifact-first approach | All intermediate and final artifacts persisted — enables offline inference |

---
*Generated by FIRE Builder Agent for work item: ml-pipeline-architecture*
