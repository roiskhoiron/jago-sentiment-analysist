---
version: 1.0.0
created: 2026-05-26T17:48:00Z
---

# Submission Validation Checklist

## Mandatory Files

| # | File | Status | Notes |
|---|------|--------|-------|
| 1 | `notebooks/01_scraping.ipynb` | [ ] | Scraping notebook |
| 2 | `notebooks/02_training.ipynb` | [ ] | Training notebook (preprocessing + training) |
| 3 | `notebooks/03_inference.ipynb` | [ ] | Inference notebook |
| 4 | `data/raw/reviews.csv` | [ ] | Raw scraped dataset (>= 10,000 rows) |
| 5 | `requirements.txt` | [x] | Created (reproducibility-policy) |
| 6 | `README.md` | [ ] | Project documentation |
| 7 | `docs/experiment-matrix.md` | [x] | Created (experiment-matrix-design) |
| 8 | `docs/evaluation-protocol.md` | [x] | Created (evaluation-protocol-definition) |
| 9 | `docs/reproducibility-policy.md` | [x] | Created (reproducibility-policy) |
| 10 | `docs/execution-roadmap.md` | [x] | Created (execution-roadmap-design) |

## Inference Output Validation

| Criteria | Requirement | Validation |
|----------|-------------|------------|
| Input | Text string (Indonesian) | String input accepted |
| Output format | Kategorikal: `Positive`, `Neutral`, `Negative` | Label output confirmed |
| Deterministic | Same input → Same output | Verified with fixed seed |

## Structure

```
submision_sentiment-analysist/
├── notebooks/
│   ├── 01_scraping.ipynb
│   ├── 02_training.ipynb
│   └── 03_inference.ipynb
├── data/
│   └── raw/
│       └── reviews.csv
├── src/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── ingest.py
│   │   ├── preprocess.py
│   │   ├── feature.py
│   │   ├── train.py
│   │   └── evaluate.py
│   └── inference.py
├── docs/
│   ├── scope.md
│   ├── target-app.md
│   ├── constraints-checklist.md
│   ├── constraint-metrics.md
│   ├── dataset-strategy.md
│   ├── labeling-strategy.md
│   ├── project-structure.md
│   ├── ml-pipeline-architecture.md
│   ├── experiment-matrix.md
│   ├── experiment-config.yaml
│   ├── evaluation-protocol.md
│   ├── reproducibility-policy.md
│   └── execution-roadmap.md
├── models/
├── reports/
├── config/
├── scripts/
├── requirements.txt
└── README.md
```
