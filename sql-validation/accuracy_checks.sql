-- =============================================================================
-- Data Quality Pillar 2: Accuracy Checks
-- Validates mathematical precision and formula correctness
-- =============================================================================

-- Check 1: Order Item Line Total Accuracy (quantity * unit_price = item_total)
SELECT 
    item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    item_total,
    ROUND(quantity * unit_price, 2) AS calculated_line_total,
    ROUND(ABS(item_total - (quantity * unit_price)), 2) AS line_variance
FROM order_items
WHERE ROUND(ABS(item_total - (quantity * unit_price)), 2) > 0.01;

-- Check 2: Order Subtotal vs Sum of Order Items
SELECT 
    o.order_id,
    o.order_number,
    o.subtotal AS header_subtotal,
    COALESCE(SUM(oi.item_total), 0.00) AS items_sum,
    ROUND(ABS(o.subtotal - COALESCE(SUM(oi.item_total), 0.00)), 2) AS subtotal_variance
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_number, o.subtotal
HAVING ROUND(ABS(o.subtotal - COALESCE(SUM(oi.item_total), 0.00)), 2) > 0.01;

-- Check 3: Total Amount Formula Accuracy (subtotal + tax_amount + shipping_fee = total_amount)
SELECT 
    order_id,
    order_number,
    subtotal,
    tax_amount,
    shipping_fee,
    total_amount,
    ROUND(subtotal + tax_amount + shipping_fee, 2) AS calculated_total,
    ROUND(ABS(total_amount - (subtotal + tax_amount + shipping_fee)), 2) AS total_variance
FROM orders
WHERE ROUND(ABS(total_amount - (subtotal + tax_amount + shipping_fee)), 2) > 0.01;
