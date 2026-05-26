# Strategi Dataset

## Rencana Scraping

### Pustaka
- **Utama**: `google-play-scraper` (Python) — ringan, tanpa browser, cepat.
- **Alternatif**: `scrapy` + `playwright` jika google-play-scraper tidak mencukupi.

### URL Target
- Halaman Google Play Store untuk Bank Jago (ID: `com.jago.android` atau ID aplikasi resmi).
- Basis: `https://play.google.com/store/apps/details?id=com.jago.android`

### Volume Target
- **Minimum**: 5.000 ulasan
- **Optimal**: 10.000+ ulasan
- **Filter**: Hanya bahasa Indonesia, semua rating (1-5 bintang)

### Format Penyimpanan: CSV
- **Kolom**: `review_id`, `review_text`, `rating`, `date`, `reviewer_id`
- **Data mentah**: `data/raw/reviews.csv`

### Pendekatan Scraping
1. Gunakan google-play-scraper untuk mengambil ulasan secara bertahap
2. Urutkan dari yang terbaru untuk mendapatkan ulasan terkini
3. Lanjutkan pengumpulan hingga volume target tercapai
4. Simpan CSV mentah ke `data/raw/`
5. Hormati batas kecepatan (jeda 1-2 detik antar batch)
