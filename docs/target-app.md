# Spesifikasi Aplikasi Target dan Volume Data

## Aplikasi Target
**Nama Aplikasi**: Bank Jago
**Platform**: Google Play Store (Android)
**Fokus**: Ulasan pengguna untuk analisis sentimen.

## Target Volume Data
**Target Minimum**: 5.000 ulasan unik pengguna berbahasa Indonesia.
**Target Optimal**: 10.000+ ulasan unik pengguna berbahasa Indonesia.
**Strategi**: Pengumpulan data awal melalui alat web scraping (misalnya Scrapy, Beautiful Soup) yang menargetkan halaman aplikasi Bank Jago di Google Play Store. Pengumpulan inkremental dapat dipertimbangkan jika volume awal tidak mencukupi atau untuk analisis deret waktu.

## Bidang Data yang Dikumpulkan
-   Teks Ulasan
-   Rating (1-5 bintang)
-   Tanggal Ulasan
-   ID Pengulas (dianonimkan jika perlu)

## Pertimbangan Kualitas Data
-   **Penyaringan Bahasa**: Memastikan hanya ulasan berbahasa Indonesia yang dikumpulkan dan diproses.
-   **Penanganan Duplikat**: Menerapkan mekanisme untuk mengidentifikasi dan menghapus ulasan duplikat.
-   **Relevansi**: Berfokus pada ulasan yang terkait langsung dengan fungsionalitas, pengalaman pengguna, dan fitur aplikasi.
