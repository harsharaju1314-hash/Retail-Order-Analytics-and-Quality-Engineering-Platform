# Power BI Analytics & Quality Engineering Reconciliation Guide
## Project: Retail Order Analytics Platform

---

### 1. Overview
The Power BI Executive Dashboard provides executive and operational visibility into retail order performance, gross/net revenue metrics, order fulfillment stages, product categories, and geographical distribution.

From a **Quality Engineering** standpoint, this dashboard serves as the target analytics interface for **Source-to-Target Data Quality Reconciliation**. Every card, chart, and matrix in this dashboard is cross-validated against PostgreSQL SQL queries to ensure 100% financial and transactional accuracy.

---

### 2. Data Model (Star Schema)

```
        +-------------------------+
        |     dim_customers       |
        +-------------------------+
        | customer_id (PK)        |
        | full_name, city, state  |
        +-------------------------+
                     | 1
                     |
                     | *
+-------------------------+           1 +-------------------------+
|       fact_orders       |-------------|      dim_products       |
+-------------------------+             +-------------------------+
| order_id (PK)           |             | product_id (PK)         |
| order_number, date      |             | product_name, category  |
| status, total_amount    |             | unit_price              |
+-------------------------+             +-------------------------+
                     | 1                         | 1
                     |                           |
                     | *                       * |
        +---------------------------------------------+
        |              fact_order_items               |
        +---------------------------------------------+
        | item_id (PK)                                |
        | order_id (FK), product_id (FK)              |
        | quantity, unit_price, item_total            |
        +---------------------------------------------+
```

---

### 3. Core Visualizations & Quality Validation Checkpoints

| Visual Name | Visual Type | Primary Metric / Measure | PostgreSQL Reconciliation Query | QA Status |
| :--- | :--- | :--- | :--- | :---: |
| **Total Orders KPI** | Card | `Total Orders = COUNTROWS('orders')` | `SELECT COUNT(*) FROM orders;` (Value: `10`) | RECONCILED |
| **Net Revenue KPI** | Card | `Net Revenue = CALCULATE(SUM('orders'[total_amount]), 'orders'[status] <> "CANCELLED")` | `SELECT SUM(total_amount) FROM orders WHERE status != 'CANCELLED';` (Value: `$2,116.73`) | RECONCILED |
| **AOV (Average Order Value)** | Card | `AOV = DIVIDE([Net Revenue], [Active Orders])` | `SELECT AVG(total_amount) FROM orders WHERE status != 'CANCELLED';` (Value: `$235.19`) | RECONCILED |
| **Orders by Status** | Donut / Bar Chart | `Orders by Status` | `SELECT status, COUNT(*) FROM orders GROUP BY status;` | RECONCILED |
| **Revenue by Category**| Clustered Bar | `Category Revenue` | `SELECT p.category, SUM(oi.item_total) FROM products p JOIN order_items oi ...` | RECONCILED |
| **Regional Sales** | Filled Map / Table | `Regional Sales` | `SELECT c.state, SUM(o.total_amount) FROM customers c JOIN orders o ...` | RECONCILED |

---

### 4. Step-by-Step QA Reconciliation Procedure
1. Export clean transactional tables from PostgreSQL (or use `powerbi/data/*.csv`).
2. Open Power BI Desktop and load the 4 normalized tables.
3. Establish 1-to-many relationships:
   - `dim_customers[customer_id]` $\rightarrow$ `fact_orders[customer_id]`
   - `fact_orders[order_id]` $\rightarrow$ `fact_order_items[order_id]`
   - `dim_products[product_id]` $\rightarrow$ `fact_order_items[product_id]`
4. Create DAX measures listed in `powerbi/dax_measures.md`.
5. Execute `sql-validation/dashboard_reconciliation.sql` in PostgreSQL.
6. Verify variance between SQL outputs and Power BI visuals is strictly **$0.00**.
