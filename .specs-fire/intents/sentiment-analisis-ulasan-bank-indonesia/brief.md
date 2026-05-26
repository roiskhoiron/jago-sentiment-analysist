---
id: sentiment-analisis-ulasan-bank-indonesia
title: Sentiment Analysis Pipeline Ulasan Bank Indonesia (Google Play)
status: completed
created: 2026-05-26T04:47:29Z
completed_at: 2026-05-26T17:50:41.556Z
---

# Intent: Sentiment Analysis Pipeline Ulasan Bank Jago Digital Banking Indonesia (Google Play)

## Goal

Membangun sistem sentiment analysis multi-kelas (Positive/Neutral/Negative) untuk ulasan pengguna aplikasi mobile banking di Indonesia dari Google Play, mulai dari scraping mandiri hingga eksperimen ML/DL yang reproducible dan inference dengan label kategorikal.

## Users

- Mahasiswa/peneliti (Anda) yang menyusun submission proyek
- Dosen/evaluator yang memverifikasi constraint, reproducibility, dan hasil eksperimen

## Problem

Membutuhkan pipeline end-to-end yang valid (tanpa dataset siap pakai) untuk mengumpulkan ulasan real, melakukan labeling yang konsisten, melatih beberapa model, mengevaluasi metrik secara benar, serta menyediakan inference yang dapat dijalankan ulang secara deterministik di Colab/Jupyter/local.

## Success Criteria

- Scraping mandiri dengan Python menghasilkan dataset ulasan real Google Play domain mobile banking (Bahasa Indonesia)
- Dataset mentah tersimpan (CSV/JSON) dengan minimal 10.000 baris dan menyertakan teks ulasan + metadata (jika tersedia: username, rating, timestamp, app)
- Pipeline preprocessing modular dan reusable (cleaning, url/emoji removal, stopword, tokenization; stemming opsional)
- Label sentimen minimal 3 kelas (Positive/Neutral/Negative) dengan aturan labeling terdokumentasi
- Minimal 3 eksperimen selesai dan terdokumentasi:
  - TF-IDF + Logistic Regression
  - TF-IDF + Linear SVM
  - Fine-tuning IndoBERT
- Setiap eksperimen melaporkan: split config, accuracy, precision, recall, F1, confusion matrix
- Akurasi testing >= 85% dan setidaknya satu eksperimen menargetkan >92% train & test (tanpa memalsukan hasil)
- Inference mengembalikan label kategorikal (Positive/Neutral/Negative) dari input teks
- Reproducible: fixed seed, artifact tersimpan (model + vectorizer/tokenizer + preprocessing), notebook berjalan berurutan tanpa modifikasi manual
- `requirements.txt` tersedia dan reproducible

## Constraints

- Dilarang menggunakan dataset publik siap pakai / Kaggle / dataset berlabel publik
- Wajib scraping dataset sendiri via Python
- Dilarang data sintetis dan dilarang memalsukan metrik
- Minimal dataset: 10.000 baris
- Minimal kelas sentimen: 3
- Minimal eksperimen: 3
- Akurasi testing minimal: 85% 
- Output inference wajib label kategorikal
- Semua notebook harus bisa dijalankan sequentially tanpa modifikasi manual

## Notes

Asumsi awal (perlu dikunci saat dekomposisi work items):
- Sumber: Google Play Store Reviews
- Target app utama: Bank Jago
  - Play Store: https://play.google.com/store/apps/details?id=com.jago.digitalBanking
  - package_id: com.jago.digitalBanking
  - target volume: ambil subset >= 10.000 (tersedia ~234k ulasan, jika scraper memungkinkan)
- Domain: mobile banking Indonesia
- Labeling awal: berbasis rating (1-2 negative, 3 neutral, 4-5 positive)
- Format deliverable: 3 notebook berurutan (01_scraping, 02_training, 03_inference)

