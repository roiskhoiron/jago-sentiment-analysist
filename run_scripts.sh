#!/usr/bin/env bash
set -euo pipefail

# run_scripts.sh — Jalankan semua script Python (.py) secara berurutan
# Pipeline: scraping -> training -> indobert -> tuning -> inference

echo "========================================"
echo "   Menjalankan pipeline Python script  "
echo "========================================"

# Cek venv
if [ -d ".venv" ]; then
    echo "[OK] .venv ditemukan"
    source .venv/bin/activate
fi

# Pastikan deps terinstall
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "[1/5] Scraping data dari Google Play Store..."
python scripts/scrape_reviews.py
echo "  -> data/raw/reviews.csv selesai"

echo ""
echo "[2/5] Training 3 model klasik (EXP-01 s/d EXP-03)..."
python scripts/run_training.py
echo "  -> models/EXP-*, reports/ selesai"

echo ""
echo "[3/5] IndoBERT base (EXP-05) — butuh GPU..."
python scripts/run_indobert.py
echo "  -> models/EXP-05_IndoBERT/ selesai"

echo ""
echo "[4/5] IndoBERT tuning (EXP-06)..."
python scripts/tune_indobert.py
echo "  -> models/EXP-06_IndoBERT_Tuned/ selesai"

echo ""
echo "[5/5] Inference demo..."
python src/inference.py "Aplikasi ini sangat membantu dan mudah digunakan"
python src/inference.py "Aplikasi sering error dan lambat"
python src/inference.py "aplikasi standar saja"

echo ""
echo "========================================"
echo " Pipeline selesai!"
echo "========================================"
