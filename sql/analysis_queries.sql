-- Example analysis queries for the Pharma Sales Insights project

-- 1. Top sellers by region and month
--    For each region and month, list the top 5 products by sales value.
WITH monthly_product_sales AS (
    SELECT
        DATE_TRUNC('month', date_id) AS month_start,
        region,
        product_id,
        SUM(sales_value) AS total_sales
    FROM fact_sales
    GROUP BY month_start, region, product_id
)
SELECT mps.month_start,
       mps.region,
       mps.product_id,
       mps.total_sales
FROM (
    SELECT mps.*, ROW_NUMBER() OVER (PARTITION BY month_start, region ORDER BY total_sales DESC) AS rn
    FROM monthly_product_sales mps
) mps
WHERE rn <= 5
ORDER BY mps.month_start, mps.region, mps.rn;

-- 2. Year‑over‑year (YoY) growth at the monthly level
--    Compare total sales for the same month across consecutive years.
WITH monthly_totals AS (
    SELECT DATE_TRUNC('month', date_id) AS month_start,
           SUM(sales_value) AS total_sales
    FROM fact_sales
    GROUP BY month_start
)
SELECT mt_this.month_start,
       mt_this.total_sales AS sales_this_year,
       mt_prev.total_sales AS sales_prev_year,
       (mt_this.total_sales - mt_prev.total_sales) / mt_prev.total_sales * 100 AS yoy_growth_pct
FROM monthly_totals mt_this
LEFT JOIN monthly_totals mt_prev
  ON mt_this.month_start = mt_prev.month_start + INTERVAL '1 year'
ORDER BY mt_this.month_start;

-- 3. Retailer concentration
--    Measure the share of sales contributed by the top retailers in each region.
WITH regional_retailer_sales AS (
    SELECT region, retailer_id, SUM(sales_value) AS retailer_sales
    FROM fact_sales
    GROUP BY region, retailer_id
), regional_totals AS (
    SELECT region, SUM(retailer_sales) AS total_sales
    FROM regional_retailer_sales
    GROUP BY region
)
SELECT rrs.region,
       rrs.retailer_id,
       rrs.retailer_sales,
       rrs.retailer_sales / rt.total_sales * 100 AS sales_share_pct
FROM regional_retailer_sales rrs
JOIN regional_totals rt
  ON rrs.region = rt.region
ORDER BY rrs.region, rrs.retailer_sales DESC;

-- 4. ABC segmentation of products based on cumulative sales contribution
--    Classify products into A/B/C categories using the 80/15/5 rule.
WITH product_totals AS (
    SELECT product_id, SUM(sales_value) AS total_sales
    FROM fact_sales
    GROUP BY product_id
), ranked_products AS (
    SELECT product_id, total_sales,
           total_sales / SUM(total_sales) OVER () AS sales_share,
           SUM(total_sales) OVER (ORDER BY total_sales DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) /
               SUM(total_sales) OVER () AS cumulative_share
    FROM product_totals
    ORDER BY total_sales DESC
)
SELECT product_id, total_sales, sales_share, cumulative_share,
       CASE
           WHEN cumulative_share <= 0.8 THEN 'A'
           WHEN cumulative_share <= 0.95 THEN 'B'
           ELSE 'C'
       END AS abc_class
FROM ranked_products;
