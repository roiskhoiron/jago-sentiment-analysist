---
version: 1.0.0
created: 2026-05-26T10:22:00Z
---

# Reproducibility Policy

## 1. Random Seed Configuration

Semua eksperimen menggunakan random seed yang terkunci untuk menjamin determinisme:

```python
import random
import numpy as np
import torch

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
```

## 2. Artifacts Wajib Disimpan

| Artifact | Description | Format | Storage Path |
|----------|-------------|--------|--------------|
| Trained Model | Model final setelah training | `.joblib` (LR/SVM), `.bin/.pth` (IndoBERT) | `models/{experiment_id}/model.{ext}` |
| Vectorizer/Tokenizer | Fitur ekstraksi object | `.joblib` / `tokenizer/` (HF) | `models/vectorizers/{experiment_id}/` |
| Preprocessing Config | Parameter preprocessing | `preprocessing_config.json` | `config/preprocessing.json` |
| Experiment Config | Konfigurasi eksperimen | `experiment_config.yaml` | `docs/experiment-config.yaml` |
| Evaluation Results | Metrics, CM, classification report | JSON, PNG, TXT | `reports/{experiment_id}/` |
| Dataset Splits | X_train, X_test, y_train, y_test | `.npy` atau `.csv` | `data/processed/{run_id}/` |

## 3. Dependency Locking

### requirements.txt

Dependency utama harus terkunci dengan versi spesifik:

```txt
# Core
python>=3.9,<3.11
numpy>=1.24,<2.0
pandas>=2.0,<3.0
scikit-learn>=1.3,<2.0
matplotlib>=3.7,<4.0
seaborn>=0.12,<1.0

# NLP
scipy>=1.10
nltk>=3.8
sastrawi>=1.0
google-play-scraper>=1.2,<2.0

# Deep Learning (optional, for IndoBERT)
transformers>=4.30,<5.0
torch>=2.0,<3.0
tokenizers>=0.13,<1.0

# Utility
joblib>=1.2,<2.0
pyyaml>=6.0,<7.0
tqdm>=4.65,<5.0
```

### Locking Method: `pip freeze > requirements.txt`
Setelah environment diverifikasi, jalankan `pip freeze > requirements.txt` untuk mengunci semua dependency.

## 4. Notebook Execution Order

Notebook harus berjalan secara sequential tanpa modifikasi manual:

```bash
# Step-by-step execution
01_scraping.ipynb      # Scrape data from Google Play
02_preprocessing.ipynb # Clean, label, split data
03_training.ipynb      # Train all experiment models
04_evaluation.ipynb    # Evaluate, compare, select best
05_inference.ipynb     # Inference demo with trained model
```

### Constraints:
- Setiap notebook menyimpan output yang dibutuhkan oleh notebook berikutnya di `data/processed/` atau `models/`
- Semua cell dapat di-run secara berurutan (Run All) tanpa error
- Tidak ada hardcoded path absolut — semua path relatif terhadap root proyek

## 5. Version Control

| Asset | VCS | Frequency |
|-------|-----|-----------|
| Source code (`.py`, `.ipynb`) | git | Setiap perubahan signifikan |
| Config files (`.yaml`, `.json`, `.toml`) | git | Setiap perubahan |
| Documentation (`.md`) | git | Setiap perubahan |
| Dataset mentah | DVC atau penyimpanan eksternal | Sekali (source of truth) |
| Dataset processed | Git LFS atau DVC | Sekali |
| Trained models | Git LFS atau cloud storage | Setiap eksperimen baru |
| `requirements.txt` | git | Setiap perubahan dependency |

## 6. Environment Reproduction

```bash
# Setup reproduction environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Or for Conda users:
conda create -n sentiment-analysis python=3.10
conda activate sentiment-analysis
pip install -r requirements.txt
```

## 7. Experiment Reproducibility Checklist

- [x] Random seed = 42 across all libraries
- [x] Train/test split dengan stratify dan random_state=42
- [x] Artifact model + vectorizer tersimpan
- [x] Config eksperimen terdokumentasi
- [x] Dependency terkunci di `requirements.txt`
- [x] Notebook sequential tanpa modifikasi manual
- [x] Path relatif digunakan (tidak ada hardcoded path absolut)

## Dependencies

- **Evaluation Protocol Definition** (evaluation-protocol-definition) ✅
- Experiment Matrix Design (experiment-matrix-design) ✅
- ML Pipeline Architecture (ml-pipeline-architecture) ✅
