## Makefile for Pharma Sales Insights

.PHONY: setup etl notebooks all

# Install Python dependencies into the current environment
setup:
	pip install -r env/requirements.txt

# Run the ETL pipeline: ingest raw data and produce aggregated metrics
etl:
	python src/ingest_clean.py
	python src/transform_metrics.py

# Execute notebooks in place with outputs using papermill
notebooks:
	papermill notebooks/01_data_cleaning_eda.ipynb notebooks/01_data_cleaning_eda.ipynb
	papermill notebooks/02_feature_engineering.ipynb notebooks/02_feature_engineering.ipynb
	papermill notebooks/03_forecasting_analysis.ipynb notebooks/03_forecasting_analysis.ipynb

# Run everything
all: setup etl notebooks
