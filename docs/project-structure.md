# Project Structure

## Directory Tree

```
sentiment-analysis/
├── config/
│   ├── config.yaml              # Main configuration file
│   └── logging.yaml             # Logging configuration
├── data/
│   ├── raw/                     # Raw scraped data (CSV)
│   ├── processed/               # Cleaned and labeled data
│   └── interim/                # Intermediate processing results
├── notebooks/                  # Jupyter notebooks (sequential execution)
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_exploration.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_evaluation.ipynb
│   └── 07_analysis.ipynb
├── src/
│   ├── data/                   # Data loading and preprocessing scripts
│   ├── pipeline/               # ML pipeline components
│   └── utils/                  # Utility functions
├── models/                     # Trained model artifacts
├── reports/
│   ├── figures/                # Generated plots and charts
│   └── tables/                 # Generated tables (CSV)
├── docs/                       # Documentation
├── scripts/                    # Standalone scripts (e.g., scrape_reviews.py)
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

## File Naming Conventions

- **Notebooks**: `XX_description.ipynb` (e.g., `01_data_collection.ipynb`)
- **Scripts**: `snake_case.py` (e.g., `scrape_reviews.py`)
- **Data Files**: `snake_case.csv/json` (e.g., `raw_reviews.csv`)
- **Models**: `model_name_version.joblib` (e.g., `nb_v1.joblib`)
- **Reports**: `YYYY-MM-DD_description.ext`

## Sequential Execution Flow

Notebooks are numbered to ensure correct execution order:
1. `01_data_collection` → Scraping
2. `02_preprocessing` → Cleaning, filtering
3. `03_exploration` → EDA
4. `04_feature_engineering` → TF-IDF, embeddings
5. `05_model_training` → Model training
6. `06_evaluation` → Model evaluation
7. `07_analysis` → Final analysis and insights