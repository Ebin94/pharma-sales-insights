-- Views for recurring business questions in the Pharma Sales Insights project

-- 1. Monthly sales trends
--    Summarise units and sales by month across all products and regions.
CREATE OR REPLACE VIEW v_monthly_trends AS
SELECT
    DATE_TRUNC('month', date_id) AS month_start,
    SUM(units_sold) AS total_units,
    SUM(sales_value) AS total_sales,
    AVG(unit_price) AS avg_unit_price
FROM fact_sales
GROUP BY month_start;

-- 2. Product performance
--    Aggregate metrics at the product level across the entire dataset.
CREATE OR REPLACE VIEW v_product_performance AS
SELECT
    product_id,
    SUM(units_sold) AS total_units,
    SUM(sales_value) AS total_sales,
    AVG(unit_price) AS avg_unit_price,
    SUM(promotion_flag) AS promo_days
FROM fact_sales
GROUP BY product_id;

-- 3. Reorder signals (simple heuristic)
--    Flag product-region combinations where the recent average units sold
--    exceeds the previous period by more than 20%.  This view assumes
--    the database supports date arithmetic similar to PostgreSQL.
CREATE OR REPLACE VIEW v_reorder_signals AS
SELECT
    fs.product_id,
    fs.region,
    AVG(CASE WHEN fs.date_id >= CURRENT_DATE - INTERVAL '30 days'
             THEN fs.units_sold END) AS avg_units_last_30,
    AVG(CASE WHEN fs.date_id <  CURRENT_DATE - INTERVAL '30 days'
              AND fs.date_id >= CURRENT_DATE - INTERVAL '60 days'
             THEN fs.units_sold END) AS avg_units_prev_30,
    CASE
        WHEN AVG(CASE WHEN fs.date_id >= CURRENT_DATE - INTERVAL '30 days' THEN fs.units_sold END) >
             1.2 * AVG(CASE WHEN fs.date_id < CURRENT_DATE - INTERVAL '30 days'
                              AND fs.date_id >= CURRENT_DATE - INTERVAL '60 days'
                             THEN fs.units_sold END)
        THEN 'Reorder'
        ELSE 'Normal'
    END AS reorder_flag
FROM fact_sales fs
GROUP BY fs.product_id, fs.region;
