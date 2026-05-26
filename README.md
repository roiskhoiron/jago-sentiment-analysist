# Sentiment Analysis Pipeline - Ulasan Bank Jago

Analisis sentimen multi-kelas (Positive/Neutral/Negative) untuk ulasan pengguna aplikasi Bank Jago di Google Play Store.

## Project Structure

```
├── notebooks/
│   ├── 01_scraping.ipynb       # Scraping data dari Google Play Store
│   ├── 02_training.ipynb       # Pelatihan model (3 eksperimen)
│   └── 03_inference.ipynb      # Demo prediksi sentimen
├── scripts/
│   ├── scrape_reviews.py       # Scraper Google Play (Python)
│   └── run_training.py         # Training pipeline script
├── src/
│   └── pipeline/               # Modul pipeline modular
├── data/
│   └── raw/reviews.csv         # Dataset hasil scraping (10.000 baris)
├── models/                     # Model dan vectorizer tersimpan
├── reports/                    # Hasil evaluasi eksperimen
├── requirements.txt            # Dependency terkunci
└── README.md
```

## Dataset

- **Sumber**: Google Play Store - Bank Jago (`com.jago.digitalBanking`)
- **Jumlah**: 10.000 ulasan (70.149 terkumpul sebelum sampling)
- **Bahasa**: Bahasa Indonesia
- **Label**: Berdasarkan rating (1-2 → Negative, 3 → Neutral, 4-5 → Positive)
- **Distribusi**: Positive 70.2%, Negative 26.7%, Neutral 3.1%

## Experiments

| Experiment | Model | Feature Extraction | Akurasi Testing |
|------------|-------|-------------------|-----------------|
| EXP-01 | Logistic Regression | TF-IDF (1-2 gram) | **87.65%** |
| EXP-02 | Linear SVM | TF-IDF (1-2 gram, extended) | **88.86%** |
| EXP-03 | Logistic Regression | Bag-of-Words | **86.95%** |
| EXP-04 | Ensemble LR+SVM | TF-IDF (1-3 gram) | **88.66%** |

Semua eksperimen mencapai akurasi testing ≥ 85%.

## Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Scraping data
```bash
python scripts/scrape_reviews.py
```
Atau buka `notebooks/01_scraping.ipynb` di Jupyter/Colab.

### 3. Training model
```bash
python scripts/run_training.py
```
Atau buka `notebooks/02_training.ipynb`.

### 4. Inference
Buka `notebooks/03_inference.ipynb` dan jalankan cell.

Atau gunakan script:
```python
from src.pipeline.inference import predict_sentiment
print(predict_sentiment("Aplikasi ini sangat membantu"))
# Output: Positive
```

## Requirements

- Python ≥ 3.9, < 3.11
- scikit-learn, pandas, numpy, matplotlib, seaborn
- google-play-scraper, nltk, sastrawi
- torch, transformers (untuk IndoBERT, jika diperlukan)

## Catatan

- **Scraping**: Menggunakan `google-play-scraper`, scraping mandiri (bukan dataset publik)
- **Reproducibility**: Random seed = 42 untuk semua eksperimen
- **Inference**: Output kategorikal (Positive/Neutral/Negative)
