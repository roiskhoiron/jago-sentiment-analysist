# Colab Guide for Sentiment Analysis Pipeline

## ❓ Apa Itu Google Colab?

**Google Colab** (Colaboratory) adalah layanan **cloud gratis** dari Google yang menyediakan **notebook Jupyter** siap pakai — langsung jalan di *browser*, tanpa perlu install Python, library, atau apapun di komputer kamu.

### Keuntungan Colab:
| Fitur | Penjelasan |
|-------|-----------|
| ✅ **No setup** | Buka browser → langsung coding. Tidak perlu install Python, pip, atau library. |
| ✅ **GPU gratis** | Dapat akses GPU (T4, V100) untuk training model machine learning — GRATIS. Ini penting untuk IndoBERT. |
| ✅ **Cloud storage** | File tersimpan di Google Drive. Bisa akses dari mana saja. |
| ✅ **Colab AI** | Ada Copilot built-in yang bisa bantu debug & autocomplete (seperti GitHub Copilot). |
| ✅ **Sudah install library populer** | PyTorch, TensorFlow, pandas, numpy, scikit-learn **sudah tersedia**. |

### Kapan Pakai Colab?
- Kamu tidak punya GPU di laptop
- Ingin coba ML tanpa install ribet
- GPU dipakai sebentar, lalu dimatikan (tidak perlu beli)

### Kapan Pakai Local?
- Dataset >1 GB (Colab batas RAM ~25 GB)
- Butuh waktu kontinu >12 jam (Colab disconnect setelah idle)
- Ingin develop cepat tanpa upload file tiap kali

---

## 🚀 Panduan Awal: Google Colab untuk Pemula

### 1. Buka Google Colab
Buka https://colab.research.google.com → klik **"File" → "Upload notebook"**

### 2. Upload Notebook dari Proyek Ini
Pilih salah satu file `.ipynb` dari folder `notebooks/` di proyek ini.

### 3. Kenali Tampilan Colab
- **Cell**: Kotak kode atau teks. Notebook terdiri dari banyak cell.
- **Run cell**: Klik tombol **▶** (play) di kiri cell, atau tekan **Shift + Enter**.
- **Runtime**: Menu paling atas → **Runtime**.

### 4. Pilih GPU (PENTING untuk IndoBERT!)
Klik **Runtime → Change runtime type → Pilih "T4 GPU"**.
Tanpa GPU, training IndoBERT akan sangat lambat (bisa 1 jam → 5-10 menit dengan GPU).

### 5. Cara Upload File ke Colab
Ada 2 cara:

**a) Upload langsung (mudah, file kecil):**
```python
from google.colab import files
uploaded = files.upload()  # Pilih file dari laptop
```

**b) Mount Google Drive (untuk file besar/simpan permanen):**
```python
from google.colab import drive
drive.mount('/content/drive')
```
Setelah itu file ada di `/content/drive/MyDrive/`.

### 6. Cara Clone Repository GitHub
```python
!git clone https://github.com/username/repo.git
%cd repo
```

### 7. Cara Install Library Tambahan
```python
!pip install nama-library
```
Tanda `!` berarti "jalankan sebagai command terminal, bukan Python".

### 8. Cara Simpan Hasil
- Hasil akan hilang saat runtime di-reset (kecuali di Google Drive).
- **Penting**: Download file sebelum tutup Colab.
```python
from google.colab import files
files.download('path/to/file.csv')
```

### 9. Runtime akan Disconnect
- Colab **idle timeout** setelah ~60-90 menit tidak ada aktivitas.
- Jika pelatihan IndoBERT belum selesai, **biarkan cell berjalan** — Colab tidak akan terputus selama code sedang running.
- Simpan model ke Drive secara periodik sebagai checkpoint.

---

## Setup untuk Proyek Ini

```bash
# 1. Install required libraries
!pip install -q google-play-scraper torch transformers accelerate datasets

# Install NLTK stopwords for Indonesian
!python -c "import nltk; nltk.download('stopwords')" 2>/dev/null || true
!pip install sastrawi
```

## Clone the Repository
```bash
!git clone https://github.com/yourusername/submision_sentiment-analysist.git
%cd submision_sentiment-analysist
```

## Install Additional Dependencies
```bash
# If using GPU runtime, install PyTorch with CUDA support
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install remaining requirements
!pip install -q pdfminer.six pyyaml tqdm
```

## Steps to Run (via Notebook)

Cara termudah: **Upload notebook (`.ipynb`) langsung ke Colab** → jalanin cell satu per satu.

### A. Clone Repo & Install Dependencies
Jalankan cell ini di awal:

```bash
!git clone https://github.com/yourusername/submision_sentiment-analysist.git
%cd submision_sentiment-analysist

!pip install -q google-play-scraper torch transformers accelerate sastrawi pandas scikit-learn joblib
!python -c "import nltk; nltk.download('stopwords')" 2>/dev/null || true
```

### B. Upload & Jalankan Notebook Langsung

| Step | Notebook | Cara | Output |
|------|----------|------|--------|
| 1 | `notebooks/01_scraping.ipynb` | Upload ke Colab, Run All | `data/raw/reviews.csv` |
| 2 | `notebooks/02_training.ipynb` | Upload ke Colab, Run All | 6 model di `models/exp-*/`, laporan di `reports/` |
| 3 | `notebooks/03_inference.ipynb` | Upload ke Colab, ganti `MODEL_DIR` sesuai model terbaik | Prediksi sentimen |

### C. Alternatif: Jalankan Script (Jika Ingin Satu Perintah)

```bash
# Scraping
!python scripts/scrape_reviews.py

# Training 3 model klasik (EXP-01 s/d EXP-03)
!python scripts/run_training.py

# IndoBERT (EXP-05) — butuh GPU
!python scripts/run_indobert.py

# Tuning IndoBERT (EXP-06)
!python scripts/tune_indobert.py

# Inference
!python src/pipeline/inference.py "Aplikasi ini sangat membantu"
```

### D. IndoBERT: Wajib GPU Runtime
Sebelum menjalankan **notebook `02_training.ipynb`** bagian IndoBERT (cell 23-30):

**Runtime → Change runtime type → Pilih "T4 GPU"** ✅

Tanpa GPU, training IndoBERT bisa memakan waktu 1-2 jam. Dengan GPU T4: ~5-10 menit.

## API Usage

### TF-IDF / SVM Model (EXP-02)
```python
from src.pipeline.inference import predict_sentiment

result = predict_sentiment("Aplikasi ini sangat membantu")
print(result)  # Output: Positive
```

### IndoBERT Models
```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def predict_indobert(text, model_path="models/EXP-06_IndoBERT_Tuned"):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=96)
    with torch.no_grad():
        outputs = model(**inputs)
    preds = torch.argmax(outputs.logits, dim=-1).item()
    labels = ["Negative", "Neutral", "Positive"]
    return labels[preds]

print(predict_indobert("Aplikasi ini sangat membantu"))  # Output: Positive
```

## Expected Results
- **Scraping**: Collects 10,000 Indonesian bank reviews
- **Training**: Produces 6 models, best accuracy 90.72% (IndoBERT)
- **Inference**: Returns sentiment label (Positive/Neutral/Negative)

## Requirements
- Python ≥ 3.9, < 3.11
- Required libraries: see `requirements.txt`

## Notes for Colab
- Use GPU runtime for faster training (Runtime → Change runtime type → GPU)
- Ensure proper file permissions when accessing Google Drive
- Clear runtime state after each execution to avoid memory issues
---

## 📂 Menjalankan ketiga notebook secara berurutan dalam satu sesi Colab

Google Colab menyimpan seluruh proyek di satu direktori (`/content/submision_sentiment-analysist`). Karena semua notebook berada di folder yang sama, kamu dapat **mengeksekusi notebook lain dari dalam notebook utama** dengan perintah `jupyter nbconvert`. Ini menjalankan notebook secara headless, menyimpan output, dan melanjutkan ke notebook berikutnya.

### Contoh sel "driver" (bisa dimasukkan di notebook baru atau di akhir `01_scraping.ipynb`)

```bash
# 1. Clone repo & masuk ke folder (jika belum dilakukan)
!git clone https://github.com/yourusername/submision_sentiment-analysist.git
%cd submision_sentiment-analysist

# 2. Install dependencies sekali
!pip install -q google-play-scraper torch transformers accelerate sastrawi pandas scikit-learn joblib
!python -c "import nltk; nltk.download('stopwords')" 2>/dev/null || true

# 3. Jalankan notebook secara berurutan
!jupyter nbconvert --to notebook --execute notebooks/01_scraping.ipynb --output exec_01.ipynb
!jupyter nbconvert --to notebook --execute notebooks/02_training.ipynb --output exec_02.ipynb
!jupyter nbconvert --to notebook --execute notebooks/03_inference.ipynb --output exec_03.ipynb

echo "Semua notebook selesai dieksekusi!"
```

### Penjelasan perintah

| Perintah | Fungsi |
|----------|--------|
| `!git clone ...` | Menduplikat seluruh repo ke sesi Colab |
| `%cd submision_sentiment-analysist` | Masuk ke direktori proyek (semua path relatif) |
| `!pip install ...` | Install semua library yang dibutuhkan |
| `!jupyter nbconvert --to notebook --execute` | Menjalankan notebook secara headless dan menyimpan hasil eksekusi ke file `exec_XX.ipynb` |

### Catatan penting

- **GPU**: Sebelum menjalankan keseluruhan pipeline, pastikan **Runtime → Change runtime type → T4 GPU** sudah dipilih. IndoBERT membutuhkan GPU.
- **Runtime tidak boleh terputus**: Proses scraping + training 6 model + inference bisa memakan waktu 15-30 menit dengan GPU. Jangan tutup tab Colab selama proses berjalan.
- **Hasil hanya bertahan selama sesi**: File akan hilang saat runtime di-reset. Setelah selesai, download artifacts penting (`models/`, `reports/`, `data/`) atau simpan ke Google Drive.
- **Error handling**: Jika satu notebook gagal (misal scraping kena rate limit), notebook berikutnya tetap akan dijalankan. Periksa file `exec_01.ipynb` untuk melihat error.

### Alternatif: Jalankan dengan Python script (lebih mudah)

Cara termudah: cukup jalankan script `.py` yang sudah ada:

```bash
!python scripts/run_training.py
!python scripts/run_indobert.py
!python scripts/tune_indobert.py
```

Script tersebut sudah melakukan training, evaluasi, dan menyimpan hasil secara otomatis.
