# Pharma Sales & Inventory Intelligence — From Data Cleaning to Tableau Insights

This project analyses five years of synthetic pharmaceutical sales data and demonstrates a realistic workflow used in commercial analytics environments. The objective was to understand demand patterns, evaluate product and regional performance, assess promotional impact and generate forecasting outputs that support stock-planning decisions. The work combines Python-based data processing, machine learning, SQL modelling, forecasting techniques and interactive Tableau reporting.

---

## Dataset Summary

The dataset contains 501,046 daily sales records between 2020-01-01 and 2024-12-31. Each entry includes product, region, retailer, units sold, price, discounts, promotions and revenue.

Key characteristics:
- 65 products across 8 ATC therapeutic categories
- 10 geographic regions and 30 retailer locations
- ~£7.16M total revenue (synthetic)
- Strong seasonality patterns linked to winter flu and summer allergy periods

The dataset was selected to approximate real stock-management and demand-planning problems faced in retail and healthcare operations.

---

## Project Structure and Approach

### 1. Data Preparation (Python)
- Loaded and cleaned raw transactional data
- Removed invalid or incomplete rows and standardised categorical fields
- Built monthly and regional aggregations for time-series and performance analysis
- Produced exploratory analysis plots

### 2. SQL Data Model
- Designed a star schema including fact and dimension tables
- Created views for reusable analytical logic such as monthly trends, ABC segmentation and top-product rankings
- Wrote example business queries for stakeholder reporting

### 3. Forecasting Models
- Evaluated seasonal patterns and created time-series features
- Model comparison using Seasonal-Naive baseline vs Gradient Boosting
- Exported six-month forecast outputs for top-selling SKUs

The simpler Seasonal-Naive model produced better accuracy than Gradient Boosting for short-term predictions, driven by strong annual seasonality. Additional feature enrichment (e.g. weather, holidays) would likely improve ML-based performance.

### 4. Tableau Insights
- Built interactive views covering sales trends, regional variations, seasonality, promotional activity and price behaviour
- Combined trend and comparison views to support business decisions such as stock allocation and promotional timing

---

## How to Run the Project

```bash
pip install -r env/requirements.txt
python src/ingest_clean.py
python src/transform_metrics.py
```

(Optional) To execute notebooks with outputs:
```bash
papermill notebooks/01_data_cleaning_eda.ipynb notebooks/01_data_cleaning_eda.ipynb
papermill notebooks/02_feature_engineering.ipynb notebooks/02_feature_engineering.ipynb
papermill notebooks/03_forecasting_analysis.ipynb notebooks/03_forecasting_analysis.ipynb
```

Forecast results:
```
data/processed/forecast_<sku>.csv
```

---

## Tableau Dashboard

Live version available here:  
https://public.tableau.com/views/Pharmacyproject_17633176318690/Sheet1?:language=en-GB

### Snapshot Preview (stored in /imgs)

| Insight | Summary | Snapshot |
| --- | --- | --- |
| Monthly Sales Trend | Seasonal peaks in Q1 and June-August; lowest Nov-Dec | ![Monthly Sales Trend](imgs/Montly-sales-trend.png) |
| Top 15 Products by Sales | Strong product concentration; Generic Painkiller 64 leads | ![Top Products](imgs/Top-15-products-by-total-sales.png) |
| Sales by ATC Category | Analgesics and NSAIDs account for most revenue | ![ATC Breakdown](imgs/Sales-Distribution-by-ATC-Category.png) |
| Seasonality Pattern | Demand repeats annually, long-term predictable | ![Seasonality Pattern](imgs/Seasonality-Pattern.png) |
| Regional Heatmap | London, South West and South East highest sales | ![Regional Heatmap](imgs/Heatmap.png) |
| Promotions vs Sales | Promotions help, but seasonal forces stronger | ![Promotional Impact](imgs/Promotional-activity-vs-Sales-impact.png) |
| Price vs Demand | Mild inverse relationship, limited elasticity | ![Price vs Demand](imgs/price_vs_demand.png) |

---

## Key Findings

- Clear seasonal behaviour supports proactive inventory planning
- Small set of SKUs drives majority of revenue (Pareto distribution)
- Sales performance varies meaningfully by region
- Promotions can increase short-term volume but are most effective when aligned with predictable demand cycles
- Baseline seasonal forecasting is highly competitive when strong seasonality exists

---

## Reflection and Next Steps

This project reinforced the value of feature understanding before model selection. The outcome where a simple seasonal approach outperformed a more complex model highlighted the importance of feature relevance over algorithm complexity. Future improvements include integrating external drivers, automating model selection and expanding ML forecasting.

---



