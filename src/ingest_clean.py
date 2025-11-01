#!/usr/bin/env python
"""Ingest and clean the raw pharma sales dataset.

This script reads the raw CSV file provided by the business,
performs a basic set of cleaning operations, and writes a
cleaned version to the processed data directory.  The cleaning
steps include:

* Parsing dates correctly
* Removing rows with missing key fields
* Filtering out negative or zero values in numerical fields
* Normalising text fields by stripping whitespace

Run this script from the repository root:

    python src/ingest_clean.py

If the raw data file is missing, the script will print an
informative message instead of raising an exception.  This makes
it clear to the user where to place the input file.
"""

from __future__ import annotations

import os
from pathlib import Path
import pandas as pd


def main() -> None:
    # Determine project root relative to this file
    base_dir = Path(__file__).resolve().parents[1]
    raw_path = base_dir / "data" / "raw" / "pharma_sales.csv"
    processed_path = base_dir / "data" / "processed" / "sales_clean.csv"

    if not raw_path.exists():
        print(
            f"Raw data file not found at {raw_path}. "
            "Please ensure 'pharma_sales.csv' is placed in the data/raw directory."
        )
        return

    # Read CSV with date parsing
    df = pd.read_csv(raw_path, parse_dates=["date"])

    # Drop rows with nulls in critical columns
    critical_cols = [
        "date",
        "product_id",
        "region",
        "retailer_id",
        "units_sold",
        "unit_price",
        "sales_value",
    ]
    df = df.dropna(subset=critical_cols)

    # Filter invalid numeric values
    df = df[(df["units_sold"] > 0) & (df["unit_price"] >= 0) & (df["sales_value"] >= 0)]

    # Normalise text columns (strip whitespace)
    for col in ["product_id", "product_name", "atc_code", "region", "retailer_id"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Ensure output directory exists and write CSV
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"Cleaned data saved to {processed_path}")


if __name__ == "__main__":
    main()
