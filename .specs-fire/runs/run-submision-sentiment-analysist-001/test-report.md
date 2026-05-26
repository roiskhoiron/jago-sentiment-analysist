# Test Report for "Project Scope Alignment"

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Project scope document approved (`docs/scope.md` created)
- [x] Target application and minimum data volume locked (`docs/target-app.md` created)

### Files Verified
- `docs/scope.md`: Contains project scope, in-scope items, out-of-scope items, key deliverables, constraints, and success metrics.
- `docs/target-app.md`: Contains target application details (Bank Jago), data volume targets (minimum 5,000, optimal 10,000+ reviews), data fields to collect, and data quality considerations.

---

## Work Item: constraint-validation

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Checklist validasi batasan tersedia (`docs/constraints-checklist.md` created)
- [x] Metrik keberhasilan tiap batasan didefinisikan (`docs/constraint-metrics.md` created)

### Files Verified
- `docs/constraints-checklist.md`: Contains 7 hard constraints with descriptions, validation status, and success metrics.
- `docs/constraint-metrics.md`: Contains detailed verification steps and pass/fail criteria for each constraint.

---

## Work Item: dataset-strategy-validation

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Rencana scraping (library, target URL, volume) divalidasi (`docs/dataset-strategy.md` created)
- [x] Format penyimpanan dataset mentah (CSV) ditetapkan
- [x] Scraping script implemented (`scripts/scrape_reviews.py`)

### Files Verified
- `docs/dataset-strategy.md`: Scraping plan with library (google-play-scraper), target URL, volume (10k reviews), CSV storage format.
- `scripts/scrape_reviews.py`: Python scraping script targeting Bank Jago with rate limiting and language filtering.

---

## Work Item: labeling-strategy-design

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Mapping rating ke label sentimen dikunci (1-2 → Neg, 3 → Neu, 4-5 → Pos)
- [x] Penanganan data netral didefinisikan

---

## Work Item: project-structure-proposal

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Struktur direktori (`notebooks/`, `data/`, `src/`, `models/`, dll.) telah dibuat
- [x] Konvensi penamaan file ditetapkan

### Files Created
- `docs/project-structure.md`: Struktur direktori dan konvensi penamaan
- Direktori: `notebooks/`, `data/raw/`, `data/processed/`, `data/interim/`, `src/`, `models/`, `reports/`, `config/`, `docs/`, `scripts/`

---

## Work Item: experiment-matrix-design

### Test Results
- **Status**: PASSED (5/5 tests)

### Acceptance Criteria Validation
- [x] Tabel konfigurasi eksperimen tersedia (`docs/experiment-matrix.md` created)
- [x] Minimal 3 model terpilih sesuai kriteria (5 models: LR, SVM, IndoBERT variants)

### Files Verified
- `docs/experiment-matrix.md`: Contains configuration table with 5 experiments, feature extraction combinations, model selection criteria, preprocessing pipeline, and reproducibility notes.
- `docs/experiment-config.yaml`: Machine-readable YAML config for all 5 experiments with targets (accuracy_testing, f1_macro), vectorizer settings, and split configs.
- `scripts/test_experiment_matrix.py`: Validation script — 5 tests all passing.

---

## Work Item: evaluation-protocol-definition

### Test Results
- **Status**: PASSED

### Acceptance Criteria Validation
- [x] Protokol evaluasi standar ditetapkan (`docs/evaluation-protocol.md` created)
- [x] Target akurasi testing >= 85% divalidasi (Section 2 — Primary Metric)

### Files Verified
- `docs/evaluation-protocol.md`: Complete evaluation protocol covering train/test split, evaluation metrics, overfitting detection, label encoding, reporting format, cross-validation, and artifact storage.
- `scripts/evaluate.py`: Evaluation module for computing metrics including accuracy, precision, recall, F1 per class and macro, plus target validation.
