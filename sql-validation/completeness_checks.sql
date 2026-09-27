-- =============================================================================
-- Data Quality Pillar 1: Completeness Checks
-- Validates that mandatory attributes are not NULL or empty
-- =============================================================================

-- Check 1: Mandatory Customer fields completeness
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state
FROM customers
WHERE first_name IS NULL OR TRIM(first_name) = ''
   OR last_name IS NULL OR TRIM(last_name) = ''
   OR email IS NULL OR TRIM(email) = ''
   OR city IS NULL OR TRIM(city) = ''
   OR state IS NULL OR TRIM(state) = '';

-- Check 2: Mandatory Order fields completeness
SELECT 
    order_id,
    order_number,
    customer_id,
    order_date,
    status,
    total_amount
FROM orders
WHERE order_number IS NULL OR TRIM(order_number) = ''
   OR customer_id IS NULL
   OR order_date IS NULL
   OR status IS NULL OR TRIM(status) = ''
   OR total_amount IS NULL;

-- Check 3: Mandatory Order Item fields completeness
SELECT 
    item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    item_total
FROM order_items
WHERE order_id IS NULL
   OR product_id IS NULL
   OR quantity IS NULL
   OR unit_price IS NULL
   OR item_total IS NULL;
