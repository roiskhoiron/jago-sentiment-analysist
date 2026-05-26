# Dokumen Ruang Lingkup Proyek

## Judul Proyek
Pipeline Analisis Sentimen untuk Ulasan Pengguna Berbahasa Indonesia (Bank Jago)

## Gambaran Umum
Proyek ini bertujuan untuk mengembangkan sistem analisis sentimen yang berfokus pada ulasan pengguna berbahasa Indonesia dari aplikasi mobile Bank Jago di Google Play Store. Sistem ini akan memanfaatkan teknik Machine Learning (ML) dan Deep Learning (DL) untuk mengklasifikasikan sentimen (positif, netral, negatif) dari data teks ulasan.

## Dalam Ruang Lingkup
-   **Pengumpulan Data**: Scraping ulasan pengguna untuk aplikasi Bank Jago dari Google Play Store.
-   **Prapemrosesan Data**: Pembersihan, tokenisasi, dan normalisasi data teks bahasa Indonesia.
-   **Pelabelan Sentimen**: Strategi pelabelan manual atau semi-otomatis untuk kategori sentimen.
-   **Pengembangan Model**: Eksperimen dengan berbagai model ML/DL (misalnya Naive Bayes, SVM, RNN, Transformer) untuk klasifikasi sentimen.
-   **Evaluasi Model**: Mendefinisikan dan menerapkan metrik evaluasi (misalnya Accuracy, Precision, Recall, F1-score) dan protokol.
-   **Reproduksibilitas**: Memastikan eksperimen dapat direproduksi melalui dokumentasi yang jelas dan kontrol versi.
-   **Pelaporan**: Menghasilkan laporan komprehensif tentang metodologi, hasil, dan wawasan.

## Di Luar Ruang Lingkup
-   **Deployment**: Deployment produksi model analisis sentimen sebagai layanan.
-   **Analisis Real-time**: Pemrosesan real-time untuk ulasan baru.
-   **Data Lintas Platform**: Pengumpulan data dari toko aplikasi selain Google Play Store (misalnya Apple App Store).
-   **Dukungan Multi-Bahasa**: Analisis di luar ulasan berbahasa Indonesia.
-   **Analisis Sentimen Berbasis Aspek**: Mengidentifikasi sentimen terhadap fitur atau aspek tertentu dari aplikasi.

## Hasil Utama
-   Dokumen Ruang Lingkup Proyek (`docs/scope.md`)
-   Spesifikasi Aplikasi Target dan Volume Data (`docs/target-app.md`)
-   Laporan Validasi Strategi Dataset
-   Dokumen Desain Strategi Pelabelan
-   Proposal Struktur Proyek
-   Desain Arsitektur Pipeline ML
-   Dokumen Desain Matriks Eksperimen
-   Definisi Protokol Evaluasi
-   Dokumen Kebijakan Reproduksibilitas
-   Desain Peta Jalan Eksekusi
-   Laporan Validasi Kemasan Submission
-   Model Analisis Sentimen (terlatih)
-   Laporan Pengujian
-   Laporan Review Kode
-   Walkthrough Implementasi

## Kendala
-   **Ketersediaan Data**: Bergantung pada aksesibilitas publik ulasan Google Play Store untuk Bank Jago.
-   **Sumber Daya Komputasi**: Terbatas pada sumber daya lokal atau cloud yang tersedia untuk pelatihan dan eksperimen model.
-   **Jadwal Waktu**: Penyelesaian proyek dalam timeline yang ditentukan.
-   **Pertimbangan Etis**: Kepatuhan terhadap panduan privasi data dan etika selama pengumpulan dan analisis data.

## Metrik Keberhasilan
-   F1-score model > 0,75 untuk klasifikasi sentimen.
-   Semua kriteria penerimaan untuk setiap item pekerjaan terpenuhi.
-   Hasil proyek selesai tepat waktu.
