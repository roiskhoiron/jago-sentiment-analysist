# Colab Guide for Sentiment Analysis Pipeline

## Overview
This guide explains how to run the sentiment analysis pipeline for Indonesian bank reviews using Google Colab.

## Setup

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

## Steps to Run

### 1. Data Scraping
```bash
# From Colab cell
!python scripts/scrape_reviews.py
```

> Note: By default scrapes Bank Jago's Google Play reviews (`com.jago.digitalBanking`). Scrapes 10,000 reviews and saves to `data/raw/reviews.csv`.

### 2. Run Training Pipeline
```bash
!python scripts/run_training.py
```

> This runs 6 experiments and produces accuracy reports in `reports/` folder.

### 3. Hyperparameter Tuning (Optional)
```bash
!python scripts/tune_indobert.py
```

### 4. Inference Demo
```bash
!python src/pipeline/inference.py "Aplikasi ini sangat membantu"
# Output: Positive

# Or run via notebook
!jupyter notebook
```

## API Usage
```python
from src.pipeline.inference import predict_sentiment

result = predict_sentiment("Aplikasi ini sangat membantu")
print(result)  # Output: Positive
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