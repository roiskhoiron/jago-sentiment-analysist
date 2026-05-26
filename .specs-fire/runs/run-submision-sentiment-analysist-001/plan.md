# Implementation Plan for "Project Scope Alignment"

### Approach
Menyelaraskan ruang lingkup proyek dengan memfokuskan pada analisis sentimen ulasan pengguna aplikasi Bank Jago di Google Play Store. Proyek ini akan mencakup pengumpulan data (scraping), pembersihan data, pelabelan, eksperimen model ML/DL, dan evaluasi hasil.

### Files to Create
- `docs/scope.md`: Dokumen ruang lingkup proyek yang mendetail.
- `docs/target-app.md`: Detail aplikasi target (Bank Jago) dan volume data target.

### Files to Modify
(none)

### Tests
- Validasi keberadaan file dokumentasi.
- Verifikasi konten dokumen sesuai dengan kriteria penerimaan.

---

## Work Item: constraint-validation

### Approach
Memvalidasi semua batasan keras proyek: (1) larangan dataset publik — scraping mandiri dari Google Play Store, (2) kewajiban scraping sendiri menggunakan tools seperti Scrapy/BeautifulSoup, (3) ambang batas akurasi minimal 85% untuk model final, (4) batasan resource komputasi, (5) etika pengambilan data.

### Files to Create
- `docs/constraints-checklist.md`: Checklist validasi batasan dengan status tiap batasan
- `docs/constraint-metrics.md`: Definisi metrik keberhasilan untuk tiap batasan

### Files to Modify
(none)

### Tests
- Validasi keberadaan file dokumentasi constraint.
- Verifikasi konten checklist dan metrik.

---

## Work Item: dataset-strategy-validation

### Approach
Memvalidasi strategi pengumpulan data menggunakan Python scraper untuk Google Play Store target aplikasi Bank Jago. Menentukan library scraping (google-play-scraper / Scrapy), target URL, volume minimal 10.000 ulasan real, dan format penyimpanan dataset mentah.

### Files to Create
- `docs/dataset-strategy.md`: Strategi pengumpulan data (library, target URL, volume, jadwal scraping)
- `scripts/scrape_reviews.py`: Python script untuk scraping ulasan Google Play Store

### Files to Modify
(none)

### Tests
- Validasi rencana scraping (library, target URL, volume).
- Verifikasi format penyimpanan dataset mentah (CSV/JSON).

---

## Work Item: labeling-strategy-design

### Approach
Mendesain strategi pelabelan sentimen berbasis rating (1-2 → negatif, 3 → netral, 4-5 → positif). Menangani data netral dan memastikan minimal 3 kelas sentimen terdefinisi dengan jelas.

### Files to Create
- `docs/labeling-strategy.md`: Dokumentasi strategi pelabelan, mapping rating-label, aturan penanganan data netral.

### Files to Modify
(none)

---

## Work Item: ml-pipeline-architecture

### Approach
Merancang arsitektur pipeline machine learning untuk analisis sentimen, meliputi ingestion, preprocessing, feature extraction, training, evaluation, dan deployment. Memilih teknologi: Python, scikit‑learn, PyTorch, MLflow, dan integrasi dengan struktur proyek modular.

### Files to Create
- `docs/ml-pipeline-architecture.md`: Dokumentasi lengkap arsitektur pipeline.
- `src/pipeline/__init__.py`
- `src/pipeline/ingest.py`
- `src/pipeline/preprocess.py`
- `src/pipeline/feature.py`
- `src/pipeline/train.py`
- `src/pipeline/evaluate.py`

### Files to Modify
- (none)

### Tests
- Pastikan setiap modul dapat di‑import tanpa error.
- Unit test untuk fungsi utama tiap modul.

---

### Approach
Mengusulkan struktur folder proyek modular untuk eksekusi notebook sequential (01_scraping → 02_preprocessing → ...) dengan direktori terpisah untuk data, notebook, source code, model artifacts, dan dokumentasi.

### Files to Create
- `docs/project-structure.md`: Dokumentasi struktur direktori dan konvensi penamaan

### Files to Modify
- (membuat direktori struktural)

### Tests
- Validasi struktur direktori sesuai proposal.
- Verifikasi konvensi penamaan file ditetapkan.

---

## Work Item: experiment-matrix-design

### Approach
Mendefinisikan matriks eksperimen minimal 3 variasi model (Logistic Regression, Linear SVM, IndoBERT) dengan kombinasi ekstraksi fitur yang berbeda. Setiap konfigurasi eksperimen mencakup: model, fitur ekstraksi, split config, target metrik (accuracy ≥85%, F1-score), dan kriteria seleksi.

### Files to Create
- `docs/experiment-matrix.md`: Tabel konfigurasi eksperimen lengkap dengan 3+ variasi model
- `docs/experiment-config.yaml` atau `config/experiments.json`: Format mesin-baca untuk reproduktibilitas

### Files to Modify
- (existing project structure)

### Tests
- Validasi tabel konfigurasi tersedia dan minimal 3 model.
- Verifikasi kriteria seleksi model terpenuhi.

---

## Work Item: evaluation-protocol-definition

### Approach
Menetapkan protokol evaluasi standar untuk semua eksperimen sentiment analysis. Protokol mencakup train/test split configuration (80/20, stratified), random seed (42), metrik evaluasi lengkap (accuracy, precision, recall, F1-score per kelas dan macro), confusion matrix, dan validasi target akurasi testing >= 85%.

### Files to Create
- `docs/evaluation-protocol.md`: Dokumentasi protokol evaluasi standar dengan definisi metrik, split config, dan prosedur penilaian
- `scripts/evaluate.py`: Module evaluasi yang dapat di-import untuk menghitung semua metrik dari model trained

### Files to Modify
- (existing project structure)

### Tests
- Validasi protokol evaluasi mencakup semua metrik yang diperlukan.
- Verifikasi target akurasi >= 85% tercatat dalam protokol.

---

### Approach
Memvalidasi semua batasan keras proyek: (1) larangan dataset publik — scraping mandiri dari Google Play Store, (2) kewajiban scraping sendiri menggunakan tools seperti Scrapy/BeautifulSoup, (3) ambang batas akurasi minimal 85% untuk model final, (4) batasan resource komputasi, (5) etika pengambilan data.

### Files to Create
- `docs/constraints-checklist.md`: Checklist validasi batasan dengan status tiap batasan
- `docs/constraint-metrics.md`: Definisi metrik keberhasilan untuk tiap batasan

### Files to Modify
(none)

### Tests
- Validasi keberadaan file dokumentasi constraint.
- Verifikasi konten checklist dan metrik.
