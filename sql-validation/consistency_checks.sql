-- =============================================================================
-- Data Quality Pillar 3: Consistency Checks
-- Validates referential integrity and foreign key relationships
-- =============================================================================

-- Check 1: Orphaned Orders (orders referencing non-existent customers)
SELECT 
    o.order_id,
    o.order_number,
    o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Check 2: Orphaned Order Items (items referencing non-existent orders)
SELECT 
    oi.item_id,
    oi.order_id
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

-- Check 3: Orphaned Product References (items referencing non-existent products)
SELECT 
    oi.item_id,
    oi.product_id
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;
