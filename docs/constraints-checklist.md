# Daftar Periksa Validasi Kendala

## Kendala Keras

| # | Kendala | Deskripsi | Status | Metrik Keberhasilan |
|---|---------|-----------|--------|---------------------|
| 1 | Tidak Ada Dataset Publik | Tidak boleh menggunakan dataset publik siap pakai (misal Kaggle, UCI). Wajib scraping mandiri. | ✅ Tervalidasi | Data dikumpulkan via scraping langsung dari Google Play Store |
| 2 | Scraping Mandiri Wajib | Proses scraping dilakukan sendiri menggunakan tools yang sesuai. | ✅ Tervalidasi | Menggunakan framework scraping (Scrapy/BeautifulSoup) untuk mengunduh data |
| 3 | Akurasi Minimum 85% | Model final harus mencapai akurasi minimal 85% pada data uji. | ✅ Terdokumentasi | Target F1-score ≥ 0,85; diukur saat fase eksperimen |
| 4 | Hanya Bahasa Indonesia | Hanya ulasan berbahasa Indonesia yang dianalisis. | ✅ Tervalidasi | Filter bahasa diterapkan saat prapemrosesan |
| 5 | Batasan Sumber Daya Komputasi | Resource terbatas pada mesin lokal/cloud yang tersedia. | ✅ Terdokumentasi | Arsitektur model disesuaikan dengan resource yang ada |
| 6 | Pengumpulan Data Etis | Data dikumpulkan secara etis, tidak melanggar ToS Google Play. | ✅ Terdokumentasi | Scraping dilakukan secara bertanggung jawab; data dianonimkan |
| 7 | Fokus Platform Tunggal | Hanya ulasan dari Google Play Store (Bank Jago). | ✅ Tervalidasi | Tidak mengambil data dari sumber/platform lain |
