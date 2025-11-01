-- Schema definition for the Pharma Sales Insights project

-- Dimension tables
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);

CREATE TABLE dim_product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    atc_code VARCHAR(20)
);

CREATE TABLE dim_region (
    region VARCHAR(100) PRIMARY KEY
);

CREATE TABLE dim_retailer (
    retailer_id VARCHAR(100) PRIMARY KEY
);

-- Fact table capturing daily transactional metrics
CREATE TABLE fact_sales (
    date_id DATE NOT NULL REFERENCES dim_date(date_id),
    product_id VARCHAR(50) NOT NULL REFERENCES dim_product(product_id),
    region VARCHAR(100) NOT NULL REFERENCES dim_region(region),
    retailer_id VARCHAR(100) NOT NULL REFERENCES dim_retailer(retailer_id),
    units_sold INT NOT NULL,
    unit_price FLOAT NOT NULL,
    discount_pct FLOAT NOT NULL,
    promotion_flag INT NOT NULL,
    sales_value FLOAT NOT NULL,
    PRIMARY KEY (date_id, product_id, region, retailer_id)
);
