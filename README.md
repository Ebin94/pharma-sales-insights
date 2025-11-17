# Pharma Sales & Inventory Intelligence — From Data Cleaning to Tableau Insights

A complete end-to-end analytics project using synthetic pharmaceutical sales data (2020–2024), demonstrating a real-world workflow from raw transaction-level data to forecasting and BI dashboarding. The project supports key business decisions related to **inventory planning, seasonality, revenue performance and promotion effectiveness**.

---

##  Executive Summary

Pharmaceutical distributors must balance demand uncertainty with inventory cost constraints.  
Excess stock leads to expiry/waste, while stock-outs cause lost sales and poor customer satisfaction.  
This project builds a scalable **analytics and forecasting framework** capable of:

- Understanding product and category performance across time and regions
- Identifying seasonality patterns and demand drivers
- Measuring the business impact of pricing and promotions
- Forecasting future demand to optimise stock levels and revenue protection
- Delivering insights in an interactive executive Tableau dashboard

---

##  Business Problem

How can we leverage historical sales patterns to forecast demand accurately and support proactive stock positioning across locations and product categories?

---

##  Project Objectives

| Objective | Delivered Through |
|----------|-------------------|
| Analyse sales behaviour & product mix | EDA, SQL views & Tableau dashboards |
| Detect seasonality & trends | Time-series analysis & monthly aggregations |
| Understand price & promotion impact | Correlation analysis & dual-axis charts |
| Forecast future sales | SARIMA & Gradient Boosting forecasting |
| Support decision-making | BI dashboards & key business recommendations |

---

##  Tech Stack

**Python (Pandas, NumPy, Matplotlib, Statsmodels, Scikit-Learn, XGBoost), SQL, Jupyter, Papermill, GitHub, Tableau**

---

##  Pipeline Overview

```
Raw Data → ETL & Cleaning → Feature Engineering → SQL & Aggregation
→ ML Forecasting → Tableau Dashboards → Insights
```

### Workflow Components

| Stage | Description |
|-------|------------|
| **ETL** | Clean raw data, remove nulls, normalise product & region values |
| **Feature Engineering** | Lag/rolling features, monthly aggregates, promo intensity |
| **Forecasting** | SARIMA & Gradient Boosting SKUs-level prediction |
| **BI Dashboards** | Tableau views for seasonality, regions, products & promotions |

---

##  Forecasting Performance Summary

- The **Seasonal Naive** model outperformed **Gradient Boosting Regressor (GBR)** on short-term forecasting due to strong yearly seasonality in demand.
- XGBoost struggled with limited feature variety—realistic for retail where external factors (weather, industry trends, holiday calendar) matter.
- This highlights opportunities to improve accuracy by introducing **causal variables & feature enrichment**.

 Forecast outputs saved to:  
`/data/processed/forecast_<sku>.csv`

---

##  Tableau Insights & Business Intelligence Layer

Interactive dashboards built in Tableau deliver insight-driven views for stakeholders across sales trends, promotions, regional behaviour and category performance.

🔗 **Live Tableau Dashboard**  
https://public.tableau.com/views/Pharmacyproject_17633176318690/Sheet1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

---

##  Dashboard Snapshots

_All images are stored in the `/imgs/` directory._

| Insight | Summary | Snapshot |
| --- | --- | --- |
| **Monthly Sales Trend (2020-2024)** | Seasonal peaks in Q1 and mid-year; weakest Nov–Dec. | ![Monthly Sales Trend](imgs/Montly-sales-trend.png) |
| **Top 15 Products by Total Sales** | Generic Painkiller 64 dominates revenue. | ![Top Products](imgs/Top-15-products-by-total-sales.png) |
| **Sales Distribution by ATC Category** | Analgesics & NSAIDs drive majority revenue. | ![ATC Breakdown](imgs/Sales-Distribution-by-ATC-Category.png) |
| **Seasonality Pattern** | Predictable multi-year cyclic behaviour. | ![Seasonality Pattern](imgs/Seasonality-Pattern.png) |
| **Regional Sales Heatmap** | London, SW, SE strongest performance. | ![Regional Heatmap](imgs/Heatmap.png) |
| **Promotional Activity vs Sales Impact** | Promotions help, but seasonal demand stronger. | ![Promotional Impact](imgs/Promotional-activity-vs-Sales-impact.png) |
| **Price vs Demand** | Mild negative elasticity. | ![Price vs Demand](imgs/price_vs_demand.png) |

---

##  Business Recommendations

| Observation | Recommendation |
|------------|---------------|
| Focus inventory planning around seasonal patterns | Avoid stockouts during peak months |
| Prioritise top SKUs (Pareto 80/20) | Maximise revenue efficiency and control inventory |
| Allocate stock by region performance | Tailored distribution strategy |
| Align promotions with seasonal peaks | Avoid ineffective blanket discounting |
| Expand feature set for ML forecasting | Weather, holidays, competitor pricing |

---

## 🔧 Reproducibility

```bash
pip install -r env/requirements.txt
python src/ingest_clean.py
python src/transform_metrics.py
```

To re-run notebooks with pre-rendered outputs:

```bash
papermill notebooks/01_data_cleaning_eda.ipynb notebooks/01_data_cleaning_eda.ipynb
papermill notebooks/02_feature_engineering.ipynb notebooks/02_feature_engineering.ipynb
papermill notebooks/03_forecasting_analysis.ipynb notebooks/03_forecasting_analysis.ipynb
```

---

##  Future Enhancements

- Add automated ML tuning & AutoML
- Deploy forecasting via REST API
- Incorporate external datasets (weather, public health indicators)
- Integrate Tableau forecasting & scenario planning
- Add anomaly detection (outlier demand weeks)

---


