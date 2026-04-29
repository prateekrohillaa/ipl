@echo off
echo ============================================
echo IPL 2026 Analytics - Pipeline Runner
echo ============================================
echo.

echo [1/6] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/6] Creating database and schemas...
python database_connection.py
echo.

echo [3/6] Extracting data from Wikipedia...
python 1.data_extraction.py
echo.

echo [4/6] Loading data into Bronze layer...
python 3.data_loading_bronze.py
echo.

echo [5/6] Cleaning data into Silver layer...
python 4.data_cleaning_silver.py
echo.

echo [6/6] Transforming data into Gold layer...
python 5.data_transform_gold.py
echo.

echo ============================================
echo Pipeline complete! Starting Streamlit dashboard...
echo ============================================
echo.
streamlit run 6.streamlit_eda.py
