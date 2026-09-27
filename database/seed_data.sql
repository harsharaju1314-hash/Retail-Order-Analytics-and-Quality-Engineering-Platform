-- =============================================================================
-- Retail Order Management Seed Data
-- =============================================================================

-- Seed Customers
INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, state, country, postal_code, created_at) VALUES
(1, 'Alice', 'Smith', 'alice.smith@example.com', '212-555-0101', 'New York', 'NY', 'USA', '10001', '2026-01-10 09:00:00'),
(2, 'Bob', 'Jones', 'bob.jones@example.com', '312-555-0102', 'Chicago', 'IL', 'USA', '60601', '2026-01-12 10:15:00'),
(3, 'Charlie', 'Brown', 'charlie.brown@example.com', '415-555-0103', 'San Francisco', 'CA', 'USA', '94105', '2026-01-15 11:30:00'),
(4, 'Diana', 'Prince', 'diana.prince@example.com', '206-555-0104', 'Seattle', 'WA', 'USA', '98101', '2026-01-18 14:20:00'),
(5, 'Evan', 'Wright', 'evan.wright@example.com', '512-555-0105', 'Austin', 'TX', 'USA', '78701', '2026-01-20 16:45:00'),
(6, 'Fiona', 'Gallagher', 'fiona.g@example.com', '617-555-0106', 'Boston', 'MA', 'USA', '02108', '2026-02-01 08:30:00'),
(7, 'George', 'Miller', 'george.m@example.com', '303-555-0107', 'Denver', 'CO', 'USA', '80202', '2026-02-05 13:10:00'),
(8, 'Hannah', 'Abbott', 'hannah.a@example.com', '404-555-0108', 'Atlanta', 'GA', 'USA', '30303', '2026-02-10 15:00:00');

-- Seed Products
INSERT INTO products (product_id, sku, product_name, category, unit_price, stock_quantity, created_at) VALUES
(1, 'SKU-ELEC-1001', 'Noise Cancelling Headphones', 'Electronics', 149.99, 50, '2026-01-01 00:00:00'),
(2, 'SKU-ELEC-1002', 'Wireless Mechanical Keyboard', 'Electronics', 89.50, 80, '2026-01-01 00:00:00'),
(3, 'SKU-ELEC-1003', 'Ultra HD Monitor 27-inch', 'Electronics', 299.00, 30, '2026-01-01 00:00:00'),
(4, 'SKU-HOME-2001', 'Stainless Steel Coffee Maker', 'Home & Kitchen', 79.95, 45, '2026-01-01 00:00:00'),
(5, 'SKU-HOME-2002', 'Non-Stick Ceramic Cookware Set', 'Home & Kitchen', 129.00, 40, '2026-01-01 00:00:00'),
(6, 'SKU-APPR-3001', 'Classic Denim Jacket', 'Apparel', 65.00, 100, '2026-01-01 00:00:00'),
(7, 'SKU-APPR-3002', 'Breathable Running Shoes', 'Apparel', 85.00, 60, '2026-01-01 00:00:00'),
(8, 'SKU-SPRT-4001', 'Adjustable Dumbbell Set', 'Sports & Outdoors', 199.50, 25, '2026-01-01 00:00:00'),
(9, 'SKU-SPRT-4002', 'Insulated Water Bottle 32oz', 'Sports & Outdoors', 24.99, 150, '2026-01-01 00:00:00'),
(10, 'SKU-HOME-2003', 'Ergonomic Desk Chair', 'Home & Kitchen', 185.00, 35, '2026-01-01 00:00:00');

-- Seed Orders
INSERT INTO orders (order_id, order_number, customer_id, order_date, status, subtotal, tax_amount, shipping_fee, total_amount, payment_method, shipping_address, created_at, updated_at) VALUES
(1, 'ORD-2026-0001', 1, '2026-02-15 10:30:00', 'DELIVERED', 239.49, 19.16, 10.00, 268.65, 'Credit Card', '100 Main St, New York, NY 10001', '2026-02-15 10:30:00', '2026-02-18 14:00:00'),
(2, 'ORD-2026-0002', 2, '2026-02-16 11:45:00', 'DELIVERED', 299.00, 23.92, 15.00, 337.92, 'Debit Card', '200 Michigan Ave, Chicago, IL 60601', '2026-02-16 11:45:00', '2026-02-20 16:30:00'),
(3, 'ORD-2026-0003', 3, '2026-02-18 14:15:00', 'SHIPPED', 144.95, 11.60, 10.00, 166.55, 'Credit Card', '300 Market St, San Francisco, CA 94105', '2026-02-18 14:15:00', '2026-02-19 09:00:00'),
(4, 'ORD-2026-0004', 4, '2026-02-20 16:00:00', 'CONFIRMED', 224.49, 17.96, 10.00, 252.45, 'PayPal', '400 Pine St, Seattle, WA 98101', '2026-02-20 16:00:00', '2026-02-20 16:05:00'),
(5, 'ORD-2026-0005', 5, '2026-02-22 09:10:00', 'PENDING', 199.50, 15.96, 15.00, 230.46, 'Credit Card', '500 Congress Ave, Austin, TX 78701', '2026-02-22 09:10:00', '2026-02-22 09:10:00'),
(6, 'ORD-2026-0006', 1, '2026-02-25 15:30:00', 'DELIVERED', 89.50, 7.16, 5.00, 101.66, 'Credit Card', '100 Main St, New York, NY 10001', '2026-02-25 15:30:00', '2026-02-28 11:20:00'),
(7, 'ORD-2026-0007', 6, '2026-03-01 12:00:00', 'CANCELLED', 129.00, 10.32, 10.00, 149.32, 'Credit Card', '600 Beacon St, Boston, MA 02108', '2026-03-01 12:00:00', '2026-03-01 14:30:00'),
(8, 'ORD-2026-0008', 7, '2026-03-05 13:40:00', 'DELIVERED', 274.50, 21.96, 15.00, 311.46, 'Debit Card', '700 17th St, Denver, CO 80202', '2026-03-05 13:40:00', '2026-03-09 17:00:00'),
(9, 'ORD-2026-0009', 8, '2026-03-10 10:20:00', 'SHIPPED', 185.00, 14.80, 15.00, 214.80, 'PayPal', '800 Peachtree St, Atlanta, GA 30303', '2026-03-10 10:20:00', '2026-03-11 08:30:00'),
(10, 'ORD-2026-0010', 3, '2026-03-15 16:50:00', 'CONFIRMED', 388.50, 31.08, 20.00, 439.58, 'Credit Card', '300 Market St, San Francisco, CA 94105', '2026-03-15 16:50:00', '2026-03-15 17:00:00');

-- Seed Order Items
INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, item_total, created_at) VALUES
-- Order 1: Alice (Headphones + Wireless Keyboard)
(1, 1, 1, 1, 149.99, 149.99, '2026-02-15 10:30:00'),
(2, 1, 2, 1, 89.50, 89.50, '2026-02-15 10:30:00'),
-- Order 2: Bob (Ultra HD Monitor)
(3, 2, 3, 1, 299.00, 299.00, '2026-02-16 11:45:00'),
-- Order 3: Charlie (Coffee Maker + Water Bottle)
(4, 3, 4, 1, 79.95, 79.95, '2026-02-18 14:15:00'),
(5, 3, 9, 2, 24.99, 49.98, '2026-02-18 14:15:00'), -- Note: 79.95 + 49.98 = 129.93 -> let's make sure sum matches subtotal exactly
-- Order 4: Diana (Headphones + Running Shoes)
(6, 4, 1, 1, 149.99, 149.99, '2026-02-20 16:00:00'),
(7, 4, 7, 1, 85.00, 85.00, '2026-02-20 16:00:00'),
-- Order 5: Evan (Adjustable Dumbbell Set)
(8, 5, 8, 1, 199.50, 199.50, '2026-02-22 09:10:00'),
-- Order 6: Alice (Wireless Keyboard)
(9, 6, 2, 1, 89.50, 89.50, '2026-02-25 15:30:00'),
-- Order 7: Fiona (Ceramic Cookware Set)
(10, 7, 5, 1, 129.00, 129.00, '2026-03-01 12:00:00'),
-- Order 8: George (Denim Jacket + Dumbbell Set + Water Bottle) -> 65 + 199.50 + 24.99 = 289.49
(11, 8, 6, 1, 65.00, 65.00, '2026-03-05 13:40:00'),
(12, 8, 8, 1, 199.50, 199.50, '2026-03-05 13:40:00'),
-- Order 9: Hannah (Desk Chair)
(13, 9, 10, 1, 185.00, 185.00, '2026-03-10 10:20:00'),
-- Order 10: Charlie (Keyboard + Ultra HD Monitor) -> 89.50 + 299.00 = 388.50
(14, 10, 2, 1, 89.50, 89.50, '2026-03-15 16:50:00'),
(15, 10, 3, 1, 299.00, 299.00, '2026-03-15 16:50:00');

-- Let's update Order 3 and Order 4 subtotals/totals to match item sums exactly:
-- Order 3: 79.95 + 49.98 = 129.93, tax (8%) = 10.39, ship = 10.00, total = 150.32
UPDATE orders SET subtotal = 129.93, tax_amount = 10.39, shipping_fee = 10.00, total_amount = 150.32 WHERE order_id = 3;
-- Order 4: 149.99 + 85.00 = 234.99, tax (8%) = 18.80, ship = 10.00, total = 263.79
UPDATE orders SET subtotal = 234.99, tax_amount = 18.80, shipping_fee = 10.00, total_amount = 263.79 WHERE order_id = 4;
-- Order 8: 65.00 + 199.50 = 264.50, tax (8%) = 21.16, ship = 15.00, total = 300.66
UPDATE orders SET subtotal = 264.50, tax_amount = 21.16, shipping_fee = 15.00, total_amount = 300.66 WHERE order_id = 8;
