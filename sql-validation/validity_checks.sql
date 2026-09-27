-- =============================================================================
-- Data Quality Pillar 5: Validity Checks
-- Validates domain values, constraints, and business ranges
-- =============================================================================

-- Check 1: Invalid Order Statuses
SELECT 
    order_id,
    order_number,
    status
FROM orders
WHERE status NOT IN ('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED');

-- Check 2: Invalid Quantities (quantity <= 0)
SELECT 
    item_id,
    order_id,
    product_id,
    quantity
FROM order_items
WHERE quantity <= 0;

-- Check 3: Invalid Negative Prices or Amounts
SELECT 
    order_id,
    order_number,
    subtotal,
    tax_amount,
    shipping_fee,
    total_amount
FROM orders
WHERE subtotal < 0 OR tax_amount < 0 OR shipping_fee < 0 OR total_amount < 0;

-- Check 4: Future Order Dates (order_date > current date)
SELECT 
    order_id,
    order_number,
    order_date
FROM orders
WHERE order_date > CURRENT_TIMESTAMP;
