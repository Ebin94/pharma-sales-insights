#!/usr/bin/env python
"""Transform the cleaned sales data into aggregated metrics for analysis.

This script reads the cleaned sales data produced by ``ingest_clean.py``
and computes monthly aggregates for each combination of product, ATC
category and region.  It also generates a set of exploratory charts
illustrating high‑level patterns in the data.  The aggregated
dataset and charts are saved into the ``data/processed`` and ``imgs``
directories respectively.

Run this script after ``ingest_clean.py``.  From the repository root:

    python src/transform_metrics.py
"""

from __future__ import annotations

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from utils import save_figure

def main() -> None:
    # Determine project root relative to this file
    base_dir = Path(__file__).resolve().parents[1]
    clean_path = base_dir / "data" / "processed" / "sales_clean.csv"
    tableau_path = base_dir / "data" / "processed" / "sales_tableau.csv"
    imgs_dir = base_dir / "imgs"

    if not clean_path.exists():
        print(
            f"Cleaned data file not found at {clean_path}. "
            "Run 'python src/ingest_clean.py' first."
        )
        return

    # Read cleaned data
    df = pd.read_csv(clean_path, parse_dates=["date"])
    # Create a month column representing the first day of each month
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Group by month, product, ATC code and region
    group_cols = ["month", "product_id", "product_name", "atc_code", "region"]
    agg_df = (
        df.groupby(group_cols)
        .agg(
            total_units=("units_sold", "sum"),
            total_sales=("sales_value", "sum"),
            avg_unit_price=("unit_price", "mean"),
            promo_days=("promotion_flag", "sum"),
        )
        .reset_index()
    )

    # Save aggregated data for Tableau or further analysis
    tableau_path.parent.mkdir(parents=True, exist_ok=True)
    agg_df.to_csv(tableau_path, index=False)

    # ----- Generate Charts -----
    # 1. Monthly Total Sales (line)
    monthly_totals = (
        agg_df.groupby("month")["total_sales"].sum().reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_totals["month"], monthly_totals["total_sales"], marker="o")
    ax.set_title("Monthly Total Sales")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    fig.autofmt_xdate()
    save_figure(fig, imgs_dir / "monthly_sales_trend.png")
    plt.close(fig)

    # 2. Top 20 Products by Sales (horizontal bar)
    top_products = (
        agg_df.groupby("product_name")["total_sales"].sum().nlargest(20).reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top_products["product_name"], top_products["total_sales"], color="skyblue")
    ax.set_title("Top 20 Products by Total Sales")
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Product Name")
    ax.invert_yaxis()
    save_figure(fig, imgs_dir / "top_products.png")
    plt.close(fig)

    # 3. Sales by ATC Category (bar)
    atc_totals = (
        agg_df.groupby("atc_code")["total_sales"].sum().sort_values(ascending=False).reset_index()
    )
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(atc_totals["atc_code"], atc_totals["total_sales"], color="coral")
    ax.set_title("Sales by ATC Category")
    ax.set_xlabel("ATC Code")
    ax.set_ylabel("Total Sales")
    ax.tick_params(axis="x", rotation=90)
    save_figure(fig, imgs_dir / "atc_breakdown.png")
    plt.close(fig)

    # 4. Seasonality: Average Monthly Sales (line)
    agg_df["month_num"] = agg_df["month"].dt.month
    seasonality = agg_df.groupby("month_num")["total_sales"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(seasonality["month_num"], seasonality["total_sales"], marker="o")
    ax.set_title("Seasonality: Average Monthly Sales")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Sales")
    ax.set_xticks(range(1, 13))
    save_figure(fig, imgs_dir / "seasonality_curve.png")
    plt.close(fig)

    # 5. Price vs Demand (scatter)
    # Sample up to 40k points for performance
    sample_df = df.sample(n=min(40000, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(
        sample_df["unit_price"], sample_df["units_sold"], alpha=0.25, s=10, color="teal"
    )
    ax.set_title("Price vs Demand (Sample)")
    ax.set_xlabel("Unit Price")
    ax.set_ylabel("Units Sold")
    save_figure(fig, imgs_dir / "price_vs_demand.png")
    plt.close(fig)

    print(
        f"Aggregated data saved to {tableau_path} and charts saved to {imgs_dir}."
    )


if __name__ == "__main__":
    main()
