-- =============================================================================
-- SQL Dashboard Reconciliation Queries
-- Cross-validates PostgreSQL Source Data against Power BI DAX Measures
-- =============================================================================

-- 1. Metric: Total Orders
-- Power BI DAX: Total Orders = COUNTROWS('orders')
SELECT 
    'Total Orders' AS metric_name,
    COUNT(*) AS postgresql_value,
    10 AS powerbi_expected_value,
    (COUNT(*) - 10) AS variance,
    CASE WHEN COUNT(*) = 10 THEN 'RECONCILED' ELSE 'DISCREPANCY' END AS reconciliation_status
FROM orders;

-- 2. Metric: Active / Net Revenue (Excluding CANCELLED)
-- Power BI DAX: Net Revenue = CALCULATE(SUM('orders'[total_amount]), 'orders'[status] <> "CANCELLED")
SELECT 
    'Net Revenue' AS metric_name,
    ROUND(SUM(total_amount), 2) AS postgresql_value,
    2307.84 AS powerbi_expected_value,
    ROUND(ABS(SUM(total_amount) - 2307.84), 2) AS variance,
    CASE WHEN ROUND(ABS(SUM(total_amount) - 2307.84), 2) = 0.00 THEN 'RECONCILED' ELSE 'DISCREPANCY' END AS reconciliation_status
FROM orders
WHERE status != 'CANCELLED';

-- 3. Metric: Gross Revenue (All Orders including Cancelled)
-- Power BI DAX: Gross Revenue = SUM('orders'[total_amount])
SELECT 
    'Gross Revenue' AS metric_name,
    ROUND(SUM(total_amount), 2) AS postgresql_value,
    2457.16 AS powerbi_expected_value,
    ROUND(ABS(SUM(total_amount) - 2457.16), 2) AS variance,
    CASE WHEN ROUND(ABS(SUM(total_amount) - 2457.16), 2) = 0.00 THEN 'RECONCILED' ELSE 'DISCREPANCY' END AS reconciliation_status
FROM orders;

-- 4. Metric: Average Order Value (AOV)
-- Power BI DAX: AOV = DIVIDE([Net Revenue], [Active Orders])
SELECT 
    'Average Order Value' AS metric_name,
    ROUND(AVG(total_amount), 2) AS postgresql_value,
    256.43 AS powerbi_expected_value,
    ROUND(ABS(AVG(total_amount) - 256.43), 2) AS variance,
    CASE WHEN ROUND(ABS(AVG(total_amount) - 256.43), 2) <= 0.01 THEN 'RECONCILED' ELSE 'DISCREPANCY' END AS reconciliation_status
FROM orders
WHERE status != 'CANCELLED';

-- 5. Metric: Orders by Status Breakdown
SELECT 
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 6. Metric: Revenue by Category
SELECT 
    p.category,
    SUM(oi.quantity) AS total_units,
    ROUND(SUM(oi.item_total), 2) AS category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'CANCELLED'
GROUP BY p.category
ORDER BY category_revenue DESC;
