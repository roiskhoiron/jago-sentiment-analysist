#!/usr/bin/env bash
set -euo pipefail

# run_notebooks.sh — Jalankan semua notebook (.ipynb) secara berurutan
# Output dieksekusi: exec_01.ipynb, exec_02.ipynb, exec_03.ipynb

echo "========================================"
echo " Menjalankan notebook secara berurutan "
echo "========================================"

# Cek venv
if [ -d ".venv" ]; then
    echo "[OK] .venv ditemukan"
    source .venv/bin/activate
fi

# Install deps jika belum
pip install -q jupyter nbconvert 2>/dev/null || true

echo ""
echo "[1/3] Menjalankan 01_scraping.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/01_scraping.ipynb --output exec_01.ipynb
echo "  -> exec_01.ipynb selesai"

echo ""
echo "[2/3] Menjalankan 02_training.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/02_training.ipynb --output exec_02.ipynb
echo "  -> exec_02.ipynb selesai"

echo ""
echo "[3/3] Menjalankan 03_inference.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/03_inference.ipynb --output exec_03.ipynb
echo "  -> exec_03.ipynb selesai"

echo ""
echo "========================================"
echo " Semua notebook selesai!"
echo " Hasil: exec_0{1,2,3}.ipynb"
echo "========================================"
