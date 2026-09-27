-- =============================================================================
-- Data Quality Pillar 4: Uniqueness Checks
-- Validates that unique constraints and business keys have no duplicates
-- =============================================================================

-- Check 1: Duplicate Order Numbers in orders table
SELECT 
    order_number,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_number
HAVING COUNT(*) > 1;

-- Check 2: Duplicate Customer Emails
SELECT 
    LOWER(email) AS normalized_email,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY LOWER(email)
HAVING COUNT(*) > 1;

-- Check 3: Duplicate Product SKUs
SELECT 
    sku,
    COUNT(*) AS duplicate_count
FROM products
GROUP BY sku
HAVING COUNT(*) > 1;
