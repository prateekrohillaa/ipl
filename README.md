# IPL 2026 Analytics Dashboard

End-to-end data pipeline: **Wikipedia → MySQL (Bronze/Silver/Gold) → Streamlit Dashboard**

## Setup

1. Install Python from [python.org](https://www.python.org/downloads/) (check "Add to PATH")
2. Open terminal in this folder and run:
   ```
   run_pipeline.bat
   ```

Or run manually:
```
pip install -r requirements.txt
python database_connection.py
python 1.data_extraction.py
python 3.data_loading_bronze.py
python 4.data_cleaning_silver.py
python 5.data_transform_gold.py
streamlit run 6.streamlit_eda.py
```

## Pipeline

| Step | File | Purpose |
|------|------|---------|
| 1 | `1.data_extraction.py` | Scrape IPL data from Wikipedia (falls back to dummy data) |
| 2 | `database_connection.py` | Create MySQL database + Bronze/Silver/Gold schemas |
| 3 | `3.data_loading_bronze.py` | Load raw CSVs into Bronze layer |
| 4 | `4.data_cleaning_silver.py` | Clean, type-cast, derive metrics → Silver layer |
| 5 | `5.data_transform_gold.py` | Aggregate & enrich → Gold layer (analysis-ready) |
| 6 | `6.streamlit_eda.py` | Interactive dashboard with charts, ML predictions, clustering |

## ML Features

- **Linear Regression**: Predict team points from wins
- **KMeans Clustering**: Group teams by performance (Strong/Average/Struggling)
- **Projections**: Projected runs for top batsmen
