# Business Requirements Document (BRD)
## Project: Retail Order Analytics & Quality Engineering Platform

---

### 1. Business Context & Objective
The Retail Order Analytics & Quality Engineering Platform is designed for retail order management, transactional processing, and business analytics reconciliation. The system processes direct consumer transactions and batch order ingestion, storing normalized records in a relational database and surfacing real-time business intelligence dashboards.

The primary objective from a Quality Engineering perspective is ensuring end-to-end data integrity, robust API validation, comprehensive UI workflow reliability, and verifiable source-to-dashboard financial reconciliation.

---

### 2. Functional Requirements (FR)

#### FR-101: Customer Management
- **FR-101.1**: The system shall allow creating customer profiles with mandatory fields (`first_name`, `last_name`, `email`, `city`, `state`).
- **FR-101.2**: Customer email must be unique and adhere to standard RFC 5322 email syntax.
- **FR-101.3**: The system shall retrieve customer details by unique `customer_id`.

#### FR-102: Order Placement & Pricing Engine
- **FR-102.1**: An order must reference an existing valid `customer_id` and contain at least one line item with valid `product_id`.
- **FR-102.2**: Order item quantities must be integers strictly greater than zero ($Q > 0$).
- **FR-102.3**: Pricing calculation rules:
  $$\text{Subtotal} = \sum (\text{item\_quantity} \times \text{unit\_price})$$
  $$\text{Tax Amount} = \text{ROUND}(\text{Subtotal} \times 0.08, 2)$$
  $$\text{Shipping Fee} = \begin{cases} \$0.00 & \text{if } \text{Subtotal} \ge \$100.00 \\ \$10.00 & \text{if } \text{Subtotal} < \$100.00 \end{cases}$$
  $$\text{Total Amount} = \text{Subtotal} + \text{Tax Amount} + \text{Shipping Fee}$$

#### FR-103: Order Lifecycle State Machine
- **FR-103.1**: Newly created orders default to `PENDING` status.
- **FR-103.2**: Allowed status transitions:
  - `PENDING` $\rightarrow$ `CONFIRMED` or `CANCELLED`
  - `CONFIRMED` $\rightarrow$ `SHIPPED` or `CANCELLED`
  - `SHIPPED` $\rightarrow$ `DELIVERED`
- **FR-103.3**: Terminal states (`DELIVERED`, `CANCELLED`) cannot transition to any other status.

#### FR-104: Order Search & Filtration
- **FR-104.1**: Users shall search orders by order number, customer name, email, or city.
- **FR-104.2**: Orders shall be filterable by status (`PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`, `CANCELLED`) and date range (`start_date`, `end_date`).

#### FR-105: AWS S3 & Lambda Batch Order Ingestion
- **FR-105.1**: The system shall ingest batch CSV order files via AWS S3 triggers.
- **FR-105.2**: The Lambda function must validate file structure, reject malformed rows, log root causes, and enrich valid rows with calculated totals.

#### FR-106: Executive Analytics & Reconciliation
- **FR-106.1**: The platform shall surface KPIs: Total Orders, Gross Revenue, Average Order Value (AOV), Orders by Status, and Revenue by Category.
- **FR-106.2**: All metrics displayed in Power BI must match PostgreSQL source data with $0.00\%$ discrepancy.

---

### 3. Acceptance Criteria Summary

| Requirement ID | Acceptance Criteria |
| :--- | :--- |
| **AC-101.1** | POST `/api/customers` with missing required field returns HTTP 400 with explicit error message. |
| **AC-101.2** | POST `/api/customers` with duplicate email returns HTTP 409 Conflict. |
| **AC-102.1** | POST `/api/orders` with non-existent `customer_id` or `product_id` returns HTTP 404 Not Found. |
| **AC-102.2** | POST `/api/orders` with item quantity $\le 0$ returns HTTP 400 Bad Request. |
| **AC-103.1** | PUT `/api/orders/{id}/status` from `DELIVERED` to `PENDING` returns HTTP 400 Invalid Transition. |
| **AC-105.1** | Lambda rejects batch rows missing mandatory headers or invalid date formats into `rejected_records`. |
| **AC-106.1** | SQL reconciliation queries match Power BI DAX calculations with $0.00$ variance. |
