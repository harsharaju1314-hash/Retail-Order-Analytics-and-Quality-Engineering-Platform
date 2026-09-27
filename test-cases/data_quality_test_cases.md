# Data Quality & SQL Test Cases (6 Core Pillars)
## Project: Retail Order Analytics & Quality Engineering Platform

---

### Pillar 1: Completeness
- **TC-DQ-COMP-001:** Check that mandatory fields in `customers` table (`first_name`, `last_name`, `email`, `city`, `state`) have zero `NULL` values.
- **TC-DQ-COMP-002:** Check that mandatory fields in `orders` table (`order_number`, `customer_id`, `order_date`, `status`, `total_amount`) have zero `NULL` values.

### Pillar 2: Accuracy
- **TC-DQ-ACC-001:** Verify that `orders.subtotal` strictly equals $\sum(\text{order\_items.item\_total})$ for every order record.
- **TC-DQ-ACC-002:** Verify that $\text{total\_amount} = \text{subtotal} + \text{tax\_amount} + \text{shipping\_fee}$ within $\$0.01$ precision.

### Pillar 3: Consistency & Referential Integrity
- **TC-DQ-CONS-001:** Detect orphan `order_items` that do not exist in the parent `orders` table.
- **TC-DQ-CONS-002:** Detect orphan `order_items` referencing non-existent `product_id`.
- **TC-DQ-CONS-003:** Verify `orders.customer_id` strictly exists in `customers.customer_id`.

### Pillar 4: Uniqueness
- **TC-DQ-UNIQ-001:** Detect duplicate `order_number` values in `orders` table.
- **TC-DQ-UNIQ-002:** Detect duplicate `email` values in `customers` table.
- **TC-DQ-UNIQ-003:** Detect duplicate `sku` values in `products` table.

### Pillar 5: Validity
- **TC-DQ-VAL-001:** Verify `orders.status` is strictly within `('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')`.
- **TC-DQ-VAL-002:** Verify `order_items.quantity` $> 0$ and `products.unit_price` $\ge 0$.
- **TC-DQ-VAL-003:** Verify all order dates are valid timestamps and not set to future dates beyond current processing day.

### Pillar 6: Timeliness
- **TC-DQ-TIME-001:** Verify latest ingested batch timestamp is within expected 24-hour ingestion window.
- **TC-DQ-TIME-002:** Verify order updated_at timestamp is greater than or equal to order created_at timestamp.

---

### Source-to-Target Reconciliation (Source CSV $\rightarrow$ PostgreSQL $\rightarrow$ Power BI)
- **TC-DQ-RECON-001:** Total records extracted from source batch equals processed rows in database.
- **TC-DQ-RECON-002:** PostgreSQL total gross revenue equals Power BI total gross revenue ($0.00\%$ variance).
- **TC-DQ-RECON-003:** PostgreSQL order counts by status match Power BI status breakdown counts.
