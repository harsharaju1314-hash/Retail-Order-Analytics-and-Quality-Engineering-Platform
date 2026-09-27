-- =============================================================================
-- SQL Analytical & Quality Engineering Validation Queries
-- Demonstrating JOINs, GROUP BY, Aggregations, Date Filters, Data Validation
-- =============================================================================

-- 1. Total Orders, Delivered Orders, and Total Gross Revenue
SELECT 
    COUNT(order_id) AS total_orders,
    COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END) AS delivered_orders,
    COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) AS cancelled_orders,
    COALESCE(SUM(total_amount), 0.00) AS total_gross_revenue,
    COALESCE(SUM(CASE WHEN status != 'CANCELLED' THEN total_amount ELSE 0 END), 0.00) AS net_revenue
FROM orders;

-- 2. Revenue by Product Category (Multi-table JOIN, GROUP BY, Aggregations)
SELECT 
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders_containing_category,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.item_total), 2) AS category_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'CANCELLED'
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 3. Customer Order History & Regional Spending (JOIN + WHERE + Aggregations)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.state,
    COUNT(o.order_id) AS total_orders,
    ROUND(COALESCE(SUM(o.total_amount), 0), 2) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.state
ORDER BY total_spent DESC;

-- 4. Monthly Order Volume and Revenue Trend (Date Filtering & Extraction)
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS order_month,
    COUNT(order_id) AS monthly_orders,
    ROUND(SUM(total_amount), 2) AS monthly_revenue
FROM orders
WHERE order_date >= '2026-01-01' AND order_date <= '2026-12-31'
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY order_month ASC;

-- 5. QA Check: Duplicate Detection (Uniqueness Validation)
-- Checks for duplicate order numbers in orders table
SELECT 
    order_number, 
    COUNT(*) AS occurrence_count
FROM orders
GROUP BY order_number
HAVING COUNT(*) > 1;

-- 6. QA Check: NULL / Missing Value Detection (Completeness Validation)
-- Finds any records with critical NULL fields
SELECT 
    'customers' AS table_name,
    COUNT(*) AS records_with_null_critical_fields
FROM customers
WHERE email IS NULL OR first_name IS NULL OR last_name IS NULL
UNION ALL
SELECT 
    'orders' AS table_name,
    COUNT(*) AS records_with_null_critical_fields
FROM orders
WHERE customer_id IS NULL OR order_number IS NULL OR status IS NULL OR total_amount IS NULL;

-- 7. QA Check: Referential Integrity & Orphaned Records (Consistency Validation)
-- Detects order items referencing non-existent orders or products
SELECT 
    oi.item_id,
    oi.order_id,
    oi.product_id
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.order_id IS NULL OR p.product_id IS NULL;

-- 8. QA Check: Order Financial Reconciliation (Accuracy Validation)
-- Reconciles order subtotal vs sum of order_items line items
SELECT 
    o.order_id,
    o.order_number,
    o.subtotal AS recorded_subtotal,
    ROUND(COALESCE(SUM(oi.item_total), 0), 2) AS calculated_items_total,
    ROUND(ABS(o.subtotal - COALESCE(SUM(oi.item_total), 0)), 2) AS discrepancy
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_number, o.subtotal
HAVING ROUND(ABS(o.subtotal - COALESCE(SUM(oi.item_total), 0)), 2) > 0.01;

-- 9. QA Check: Record Count Source-to-Target Validation
SELECT 
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM orders) AS total_orders,
    (SELECT COUNT(*) FROM order_items) AS total_order_items;
