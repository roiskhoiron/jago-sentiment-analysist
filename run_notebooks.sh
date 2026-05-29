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

echo "[0/3] Menyiapkan lingkungan..."
# install deps jika belum
# 1. Install required libraries
pip install -q google-play-scraper torch transformers accelerate sastrawi pandas scikit-learn joblib

# Install NLTK stopwords for Indonesian
python -c "import nltk; nltk.download('stopwords')" 2>/dev/null || true
pip install sastrawi

# If using GPU runtime, install PyTorch with CUDA support
pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install remaining requirements
pip install -q pdfminer.six pyyaml tqdm


echo ""
echo "[1/3] Menjalankan 01_scraping.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/01_scraping.ipynb --output 01_scraping.ipynb
echo "  -> exec_01.ipynb selesai"

echo ""
echo "[2/3] Menjalankan 02_training.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/02_training.ipynb --output 02_training.ipynb
echo "  -> exec_02.ipynb selesai"

echo ""
echo "[3/3] Menjalankan 03_inference.ipynb..."
jupyter nbconvert --to notebook --execute notebooks/03_inference.ipynb --output 03_inference.ipynb
echo "  -> exec_03.ipynb selesai"

echo ""
echo "========================================"
echo " Semua notebook selesai!"
echo " Hasil: exec_0{1,2,3}.ipynb"
echo "========================================"

# Git setup untuk Colab (PAT-based, non-interaktif)
if [ ! -d ".git" ]; then
    echo "[0.5/3] Menginisialisasi git repo..."
    git init
fi

git config user.name "${GIT_USER_NAME:-Colab User}"
git config user.email "${GIT_USER_EMAIL:-colab@user.com}"

# Bangun URL dengan PAT jika tersedia
if [ -n "${GIT_PAT:-}" ]; then
    REMOTE_URL="https://${GIT_PAT}@github.com/roiskhoiron/jago-sentiment-analysist.git"
else
    REMOTE_URL="${GIT_REPO_URL:-https://github.com/roiskhoiron/jago-sentiment-analysist.git}"
fi

# Set remote origin jika belum ada
if ! git remote | grep -q "^origin$"; then
    echo "[0.5/3] Menambahkan remote origin..."
    git remote add origin "$REMOTE_URL"
else
    git remote set-url origin "$REMOTE_URL"
fi

echo "Finalizing... Git add all generated file and changes to push to GitHub"
git add .

# Skip commit jika tidak ada perubahan (file belum berubah)
if ! git diff --cached --quiet; then
    git commit -m "Update generated notebooks and results"
fi

git push origin master 2>/dev/null || git push -u origin master

echo "Done!"
echo "========================================"
echo " Pipeline selesai!"
echo "========================================"

