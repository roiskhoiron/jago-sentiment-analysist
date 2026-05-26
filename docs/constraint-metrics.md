# Metrik Keberhasilan Kendala

## Definisi Metrik

### C1: Tidak Ada Dataset Publik
- **Verifikasi**: Pastikan tidak ada referensi ke Kaggle, UCI, atau repositori dataset publik lainnya dalam kode atau dokumentasi.
- **Lulus**: Semua titik pemuatan data merujuk pada file `.csv`/`.json` hasil scraping lokal.
- **Gagal**: Adanya impor atau referensi ke dataset publik yang dikenal.

### C2: Scraping Mandiri Wajib
- **Verifikasi**: Skrip scraping ada di repositori (misalnya `scripts/scrape_reviews.py`).
- **Lulus**: Skrip berjalan sukses dan menghasilkan output dengan ≥5.000 ulasan.
- **Gagal**: Tidak ada skrip scraping atau skrip gagal menghasilkan volume data minimal.

### C3: Akurasi Minimum 85%
- **Verifikasi**: Evaluasi model final pada set uji yang ditahan.
- **Lulus**: F1-score ≥ 0,85 pada set uji.
- **Gagal**: F1-score < 0,85 → lakukan iterasi pada model atau data.

### C4: Hanya Bahasa Indonesia
- **Verifikasi**: Deteksi bahasa diterapkan selama prapemrosesan.
- **Lulus**: <5% ulasan non-Indonesia dalam dataset final.
- **Gagal**: ≥5% ulasan non-Indonesia → tingkatkan filter bahasa.

### C5: Batasan Sumber Daya Komputasi
- **Verifikasi**: Arsitektur model tidak boleh melebihi 8GB RAM atau 4 core CPU (atau sesuai definisi lingkungan).
- **Lulus**: Pelatihan selesai dalam batasan sumber daya.
- **Gagal**: Kehabisan memori atau waktu proses berlebihan → optimalkan model.

### C6: Pengumpulan Data Etis
- **Verifikasi**: Scraping menghormati `robots.txt`, batas kecepatan, dan menganonimkan ID pengulas.
- **Lulus**: Implementasi mencakup pembatasan kecepatan dan anonimisasi ID.
- **Gagal**: Tidak ada pembatasan kecepatan atau anonimisasi → tambahkan sebelum pengumpulan.

### C7: Fokus Platform Tunggal
- **Verifikasi**: Semua pemuatan data dan scraping hanya menargetkan halaman Google Play Store Bank Jago.
- **Lulus**: Tidak ada referensi ke platform atau aplikasi lain.
- **Gagal**: Data dari platform lain terdeteksi → hapus dan batasi ruang lingkup.
