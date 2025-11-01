# Methodology

This document describes the technical approach taken to build the **Pharma Sales & Inventory Intelligence** project.  The goal of the project is to ingest a transactional dataset of synthetic pharmaceutical sales, cleanse and transform the data into a tidy analytical format, explore patterns and trends, engineer predictive features, and ultimately produce a set of dashboards and forecasts that can inform business decision‑making.

## Data Ingestion & Cleaning

The raw dataset (`pharma_sales.csv`) contains daily transactions between pharmaceutical suppliers and retailers from 2020‑01‑01 to 2024‑12‑31.  Each record includes the date, product identifier and name, Anatomical Therapeutic Chemical (ATC) classification, geographic region, retailer identifier, units sold, unit price, discount percentage, promotion flag, and the computed sales value.  

The ingestion script performs the following operations:

1. **Date Parsing:** The `date` column is parsed into a proper `datetime` type so that monthly grouping and time‑series operations are accurate.
2. **Null Filtering:** Rows with missing values in critical fields (`date`, `product_id`, `region`, `retailer_id`, `units_sold`, `unit_price`, `sales_value`) are removed to avoid incomplete records skewing aggregates.
3. **Value Filtering:** Observations where `units_sold` is non‑positive or prices/sales are negative are discarded as invalid.
4. **Text Normalisation:** String columns are trimmed of extra whitespace to ensure consistent keys.

The result is a clean dataset stored in `data/processed/sales_clean.csv` that serves as the foundation for all subsequent analysis.

## Transformation & Aggregation

To support efficient analysis and visualisation, the cleaned data is aggregated to the monthly level.  The script `transform_metrics.py` groups the transactions by month (`date` truncated to the first day of the month), `product_id`, `product_name`, `atc_code`, and `region`.  Four summary metrics are computed:

| Metric        | Definition                                                      |
|--------------|-----------------------------------------------------------------|
| **total_units** | Sum of `units_sold` for all transactions in the group            |
| **total_sales** | Sum of `sales_value` (units × price × (1 − discount))            |
| **avg_unit_price** | Mean of `unit_price`, capturing the typical selling price      |
| **promo_days** | Count of days with `promotion_flag = 1`, indicating promotions |

This aggregated dataset (`data/processed/sales_tableau.csv`) is used both for exploratory analysis and as input to feature engineering and forecasting.

## Exploratory Data Analysis (EDA)

EDA examines the high‑level characteristics of the sales data.  Key visualisations include:

- **Monthly Total Sales:** A line chart displaying the total sales value across all products and regions by month, revealing growth trends and seasonal peaks.
- **Top Products:** A horizontal bar chart ranking the top 20 products by cumulative sales value.
- **ATC Breakdown:** A bar chart summarising sales by ATC category, highlighting which therapeutic classes drive the majority of revenue.
- **Seasonality Curve:** A line chart of the average sales by calendar month (aggregated over years), showing seasonal demand patterns for the portfolio.
- **Price vs Demand:** A scatter plot of unit price versus units sold for a 40k‑sample, illustrating the degree of price elasticity in the synthetic market.

These visuals are generated programmatically and saved into the `imgs/` directory.  They are embedded in the README to provide an at‑a‑glance summary for stakeholders.

## Feature Engineering

Forecasting future sales requires transforming the aggregated monthly data into a supervised learning format.  The feature engineering notebook constructs the following attributes:

- **Lag Features (`lag_1`, `lag_3`, `lag_6`):** The sales value from one, three and six months prior, capturing temporal autocorrelation.
- **Rolling Means (`rolling_3`, `rolling_6`):** The average sales over the preceding three and six months, smoothing out short‑term volatility.
- **Calendar Features:** Month of year and year indicators to model seasonality and long‑term growth.
- **Promotion Intensity:** The number of promotional days in the month (`promo_days`), reflecting marketing activity.
- **Price Signal:** The average unit price (`avg_unit_price`) to capture price elasticity.

A correlation matrix and feature‑importance plot (from a simple XGBoost model) are used to assess which variables are most predictive of future sales.

## Forecasting Methodology

The forecasting analysis focuses on the top SKUs by historical sales.  For each selected product, two approaches are implemented:

1. **SARIMA Baseline:** A seasonal ARIMA model with parameters (1,1,1) × (1,1,1,12) is fit on the training portion of the time series.  The model captures seasonal patterns and trends.  A six‑step ahead forecast is produced along with confidence intervals.
2. **XGBoost Regressor:** Using the engineered lag, rolling and calendar features, an XGBoost regression model is trained on time‑ordered data (no shuffling).  The model forecasts the next six months of sales.  For horizon forecasting, predicted values are fed back into the feature set iteratively.

Model performance is evaluated on a hold‑out period using the Mean Absolute Percentage Error (MAPE).  The final notebook presents both the numeric evaluation and visual plots comparing the actual versus forecasted values.

The outputs of each forecast (actual and predicted values for each horizon) are saved as CSV files (`data/processed/forecast_<sku>.csv`), which can be fed into downstream reporting tools or dashboards.
