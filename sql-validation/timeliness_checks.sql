-- =============================================================================
-- Data Quality Pillar 6: Timeliness Checks
-- Validates data currency, latency, and chronological order
-- =============================================================================

-- Check 1: Ingestion Latency / Max Order Date
SELECT 
    MAX(order_date) AS most_recent_order_timestamp,
    CURRENT_TIMESTAMP AS current_validation_time,
    ROUND(CAST(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(order_date))) / 3600 AS NUMERIC), 2) AS hours_since_last_order
FROM orders;

-- Check 2: Chronological Integrity (updated_at must be >= created_at)
SELECT 
    order_id,
    order_number,
    created_at,
    updated_at
FROM orders
WHERE updated_at < created_at;
