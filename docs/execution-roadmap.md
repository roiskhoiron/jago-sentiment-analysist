---
version: 1.0.0
created: 2026-05-26T17:32:00Z
---

# Execution Roadmap

## Overview

Roadmap teknis untuk implementasi Sentiment Analysis Pipeline dari scraping hingga inference demo. Mengikuti urutan notebook sequential.

## Phases & Timeline

| Phase | # | Task | Deliverable | Estimated Duration | Dependencies |
|-------|---|------|-------------|-------------------|--------------|
| **Scraping** | 1 | Scrape ulasan Bank Jago dari Google Play Store | `data/raw/reviews.csv` (~10k rows) | 1-2 hours | - |
| **Preprocessing** | 2 | Clean text, remove URL/emoji, stopword removal, stemming, label encoding | `data/processed/clean_reviews.csv`, `config/preprocessing.json` | 1 hour | Phase 1 |
| **Feature Extraction** | 3 | Generate TF-IDF, BoW, and IndoBERT embeddings | `data/processed/features/` | 1 hour | Phase 2 |
| **Training** | 4 | Train LR, SVM, IndoBERT models with configs | `models/exp-*/`, trained artifacts | 2-4 hours (GPU advised for IndoBERT) | Phase 3 |
| **Evaluation** | 5 | Evaluate all models, generate metrics, confusion matrices, select best model | `reports/exp-*/`, `reports/comparison.md` | 1 hour | Phase 4 |
| **Inference** | 6 | Build inference demo with input text → sentiment label | `notebooks/05_inference.ipynb`, `src/inference.py` | 1 hour | Phase 5 |
| **Packaging** | 7 | Final validation, fix issues, package deliverables | `submission/` folder with all artifacts | 1 hour | Phase 6 |

## Notebook Sequence

```bash
# Sequential execution (mandatory)
01_scraping.ipynb       → data/raw/reviews.csv
02_preprocessing.ipynb  → data/processed/clean_reviews.csv
03_training.ipynb       → models/*, reports/*
04_evaluation.ipynb     → reports/comparison.md
05_inference.ipynb      → inference output
```

## Checkpoints

| Checkpoint | Phase(s) | Validation | Gate |
|------------|----------|------------|------|
| CP-1 | Scraping | Dataset >= 10,000 rows, valid CSV format | Y: Continue / N: Fix scraping |
| CP-2 | Preprocessing | Clean text, correct labels, balanced classes | Y: Continue / N: Fix preprocessing |
| CP-3 | Training | All 3 models trained without errors | Y: Continue / N: Fix training |
| CP-4 | Evaluation | Accuracy >= 85%, metrics match targets | Y: Continue / N: Tune hyperparameters |
| CP-5 | Inference | Input text → correct sentiment label | Y: Package / N: Fix inference |

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scraping rate-limited | Medium | High | Use google-play-scraper with delay, pagination |
| GPU not available for IndoBERT | Medium | High | Fallback to CPU with batch_size=8; allow longer runtime |
| Imbalanced classes | High | Low | Use stratified split SMOTE or class weights |
| Notebook out-of-order run | Low | Critical | Test sequential execution after each phase |

## Deliverables

| Asset | Location | Format |
|-------|----------|--------|
| Raw dataset | `data/raw/reviews.csv` | CSV |
| Clean dataset | `data/processed/clean_reviews.csv` | CSV |
| Trained models | `models/exp-{id}/model.{ext}` | .joblib/.bin |
| Evaluation reports | `reports/exp-{id}/metrics.json` | JSON |
| Inference script | `src/inference.py` | Python |
| Submission package | `submission/` | Folder |

## >92% Accuracy Strategy

Target akurasi >92% memerlukan pendekatan khusus melampaui baseline 85%:

| Approach | Method | Expected Gain | Applied To |
|----------|--------|---------------|------------|
| **Transformer fine-tuning** | IndoBERT with learning rate scheduling, warmup, and early stopping | +5-8% over baseline | EXP-03 |
| **Hyperparameter optimization** | Grid search on SVM C/gamma and LR regularization | +2-3% over default | EXP-02, EXP-05 |
| **Feature engineering** | Trigram TF-IDF + stemming (Sastrawi) | +1-2% over bigram | EXP-05 |
| **Ensemble** | Soft voting (LR + SVM + IndoBERT) | +1-3% over single model | Post-EXP comparison |
| **Data augmentation** | Back-translation or synonym replacement for minority classes | +1-2% F1 on neutral | If class imbalance >2:1 |

**Execution order for >92%:**
1. Train LR baseline (EXP-01) → validate reachable accuracy
2. Train SVM with grid search (EXP-02, EXP-05) → select best SVM variant
3. Fine-tune IndoBERT (EXP-03) → if >=92%, select as final
4. If <92%: build ensemble (LR + SVM + IndoBERT soft voting)
5. If still <92%: apply data augmentation for neutral class, re-train ensemble
