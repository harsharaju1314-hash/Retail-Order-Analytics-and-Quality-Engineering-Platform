# Retail Order Analytics & Quality Engineering Platform

A full-lifecycle retail order management, batch data processing, and quality engineering platform built with Python, Flask, PostgreSQL, AWS S3/Lambda data workflows, Power BI analytics, and automated testing across API, UI, and Data Quality dimensions.

---

## Overview

In retail and e-commerce enterprises, transactional order systems must maintain strict data integrity across order capture, batch file ingestion, database storage, and analytical dashboards. A failure in data validation or state transitions can result in financial inaccuracies, incorrect inventory counts, or misleading executive reporting.

This project was built to demonstrate end-to-end **Quality Engineering (QE) and Data Quality Validation** principles across a realistic retail order processing pipeline. It combines a relational transactional backend, a serverless batch ingestion simulation, automated functional and regression test suites, cross-system data reconciliation, and executive business intelligence.

---

## Problem Statement

Retail applications face several common data quality and operational risks:
1. **API Validation Gaps**: Accepting invalid orders with negative quantities, non-existent customer/product foreign keys, or empty request payloads.
2. **State Machine Violations**: Unauthorized or illogical status transitions (e.g., transitioning a `DELIVERED` or `CANCELLED` order back to `PENDING`).
3. **Batch Ingestion Corruption**: Upstream CSV batch files containing missing mandatory columns, invalid dates, malformed statuses, or duplicate order IDs.
4. **Data Drift & Financial Misstatements**: Discrepancies between PostgreSQL transactional records and Power BI analytical measures due to incorrect filtering or floating-point precision issues.

This platform implements automated controls, schema constraints, validation routines, and cross-system reconciliation queries to eliminate these failure modes.

---

## Key Features

- **Relational Order Engine**: Normalized 3NF PostgreSQL schema managing `customers`, `products`, `orders`, and `order_items`.
- **RESTful API Service**: Flask API endpoints supporting order placement, customer management, status updates, and multi-criteria filtering.
- **Strict Business Validation Layer**: Validates required fields, positive integer quantities, foreign key integrity, valid status state machine transitions, and date formatting.
- **AWS Batch Processing Workflow**: AWS Lambda data validation handler processing order CSV files from S3, isolating clean records and logging rejected rows with specific error codes.
- **Power BI Executive Dashboard & Reconciliation**: Tabular data model with DAX measures cross-validated against PostgreSQL SQL queries with $0.00\%$ discrepancy.
- **Playwright UI Test Automation**: 10 automated browser tests validating authentication, search, filtering, order inspection, and status management.
- **Data Quality Test Suite (6 Pillars)**: Automated SQL verification covering Completeness, Accuracy, Consistency, Uniqueness, Validity, and Timeliness.
- **Automated CI/CD**: GitHub Actions pipeline that installs dependencies, executes the test suite, and outputs formatted execution reports.
- **Defect Management**: Jira-aligned defect logging detailing root cause analysis and resolution workflows for UI, API, Data Quality, and Dashboard defects.

---

## Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend & APIs** | Python 3.12, Flask, SQLAlchemy | Application server, REST API endpoints, business validation logic |
| **Database** | PostgreSQL, SQL (SQLite for local test harness) | Relational persistence, constraints, analytical queries |
| **Batch Processing** | AWS S3, AWS Lambda (Python runtime) | Serverless batch file ingestion, schema validation, record enrichment |
| **UI Automation** | Playwright (Python), Chromium | Headless browser end-to-end functional testing |
| **Test Automation** | Pytest, Requests | Unit, API, Data Quality, and Integration test suites |
| **API Testing** | Postman | Exportable Collection v2.1 with JavaScript test assertions |
| **Analytics & BI** | Power BI, DAX | Business metrics, category breakdown, regional analytics |
| **Reporting & Defect Tracking**| Microsoft Excel (openpyxl), Jira | Test execution matrix, defect lifecycle tracking |
| **CI/CD** | GitHub Actions | Automated build, testing, and report generation |

---

## System Architecture & Workflow

The platform follows a simple, decoupled data and request flow:

```
[ Web Browser (UI) ]      [ REST API Client (Postman) ]      [ Batch CSV File ]
         |                              |                             |
         v                              v                             v
+------------------+          +-------------------+          +------------------+
| Flask Web Router |          |   REST API Layer  |          |   AWS S3 Bucket  |
+------------------+          +-------------------+          +------------------+
         |                              |                             |
         +--------------+---------------+                             v
                        |                                    +------------------+
                        v                                    |    AWS Lambda    |
             +--------------------+                          | Data Validation  |
             | Validation Service |                          +------------------+
             +--------------------+                                   |
                        |                                             |
                        +----------------------+----------------------+
                                               |
                                               v
                                    +---------------------+
                                    | PostgreSQL Database |
                                    | (3NF Relational DB) |
                                    +---------------------+
                                               |
                                               v
                                    +---------------------+
                                    |  Power BI Dashboard |
                                    | (Source Reconciled) |
                                    +---------------------+
```

### Core Execution Flows
1. **Online Order Flow**: User / Client $\rightarrow$ REST API $\rightarrow$ Validation Service $\rightarrow$ PostgreSQL $\rightarrow$ JSON / HTML Response.
2. **Batch Ingestion Flow**: CSV File $\rightarrow$ AWS S3 $\rightarrow$ Lambda Trigger $\rightarrow$ Row Validation & Math Enrichment $\rightarrow$ Processed Records.
3. **Reconciliation Flow**: PostgreSQL SQL Aggregation $\leftrightarrow$ Power BI DAX Measures $\rightarrow$ Data Quality Audit Log ($0.00\%$ variance).

---

## Project Structure

```text
Retail-Order-Analytics-and-Quality-Engineering-Platform/
├── .github/
│   └── workflows/
│       └── ci.yml                         # GitHub Actions CI automated pipeline
├── app/
│   ├── __init__.py                        # Flask application factory
│   ├── database.py                        # Database connection & session management
│   ├── models.py                          # SQLAlchemy ORM models (Customer, Product, Order, OrderItem)
│   ├── routes_api.py                      # REST API endpoints & error handlers
│   ├── routes_web.py                      # Web UI controllers & session authentication
│   ├── validation.py                      # Core business rules & input validation logic
│   ├── static/
│   │   ├── css/styles.css                 # Custom responsive stylesheet
│   │   └── js/app.js                      # Dynamic frontend scripts
│   └── templates/
│       ├── base.html                      # Base UI layout & navigation
│       ├── login.html                     # Portal authentication view
│       ├── orders.html                    # Order list, search, & filter interface
│       ├── order_detail.html              # Itemized order details & status manager
│       ├── create_order.html              # Manual order entry form
│       └── analytics.html                 # Cross-system BI reconciliation dashboard
├── aws/
│   ├── lambda_function.py                 # AWS Lambda batch validation handler
│   ├── test_lambda.py                     # Pytest suite for Lambda data quality rules
│   ├── simulate_s3_pipeline.py            # Local simulation runner for S3->Lambda pipeline
│   └── sample_s3_events/
│       ├── batch_orders_valid.csv         # Clean batch test input
│       ├── batch_orders_corrupted.csv     # Corrupted batch test input (anomaly injection)
│       └── s3_put_event.json              # Sample S3 trigger event payload
├── database/
│   ├── schema.sql                         # PostgreSQL 3NF DDL schema
│   ├── seed_data.sql                      # Realistic sample relational seed data
│   └── queries.sql                        # Analytical, aggregation, & QA validation SQL queries
├── defects/
│   ├── DEFECTS_LOG.md                     # Jira-format defect logs (RET-101 through RET-104)
│   ├── defect_lifecycle.md                # Defect triage workflow & severity matrix
│   └── jira_export_defects.csv            # Jira-compatible CSV defect export
├── postman/
│   ├── Retail_Order_API_Collection.json   # Postman Collection v2.1 with automated tests
│   └── Retail_Order_API_Environment.json  # Postman environment configuration
├── powerbi/
│   ├── README.md                          # Power BI Star Schema architecture & QA guide
│   ├── dax_measures.md                    # DAX measure definitions & SQL mapping
│   └── data/                              # Source datasets for Power BI ingestion
│       ├── customers_dataset.csv
│       ├── products_dataset.csv
│       ├── orders_dataset.csv
│       └── order_items_dataset.csv
├── reports/
│   └── Retail_Order_Test_Execution_Report.xlsx # Generated multi-tab Excel test execution sheet
├── requirements/
│   ├── BRD_Retail_Order_Management.md     # Business Requirements Document & Acceptance Criteria
│   └── RTM_Requirement_Traceability_Matrix.md # Requirement Traceability Matrix (RTM)
├── scripts/
│   ├── init_db.py                         # Database initialization & seed utility
│   ├── generate_excel_report.py           # Automated Excel test report generator
│   └── run_reconciliation.py              # CLI reconciliation audit utility
├── sql-validation/
│   ├── completeness_checks.sql            # Data Quality: Completeness tests
│   ├── accuracy_checks.sql                # Data Quality: Mathematical accuracy tests
│   ├── consistency_checks.sql             # Data Quality: Referential consistency tests
│   ├── uniqueness_checks.sql              # Data Quality: Duplicate detection tests
│   ├── validity_checks.sql                # Data Quality: Domain validity tests
│   ├── timeliness_checks.sql              # Data Quality: Data recency & SLA tests
│   └── dashboard_reconciliation.sql       # SQL queries for Power BI reconciliation
├── tests/
│   ├── conftest.py                        # Pytest fixtures & Playwright live server harness
│   ├── api/
│   │   ├── test_customers_api.py          # Customer API test suite
│   │   ├── test_orders_api.py             # Order API test suite
│   │   └── test_api_error_handling.py     # Negative, boundary, & error handling tests
│   ├── data_quality/
│   │   ├── test_data_integrity.py         # 6 Pillars Data Quality automated tests
│   │   └── test_source_target_reconciliation.py # SQL to Benchmark reconciliation tests
│   ├── ui/
│   │   └── test_ui_flows.py               # Playwright automated UI browser tests
│   └── unit/
│       └── test_validation.py             # Business rule & state machine unit tests
├── pytest.ini                             # Pytest configuration file
├── requirements.txt                       # Python dependencies
├── run.py                                 # Application entry point
└── README.md
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/harsharaju1314-hash/Retail-Order-Analytics-and-Quality-Engineering-Platform.git
cd Retail-Order-Analytics-and-Quality-Engineering-Platform
```

### 3. Create and Activate Virtual Environment
```bash
# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies & Playwright Browsers
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 5. Initialize & Seed Database
```bash
python scripts/init_db.py --reset
```

---

## Running the Application

Start the local Flask development server:
```bash
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

### Demo Login Credentials
- **Email:** `admin@retail.com`
- **Password:** `Admin123!`

---

## REST API Endpoints

| Method | Endpoint | Purpose | Request Body / Query Params | Status Codes |
| :---: | :--- | :--- | :--- | :---: |
| `POST` | `/api/customers` | Register a new customer | JSON: `first_name`, `last_name`, `email`, `city`, `state` | `201`, `400`, `409` |
| `GET` | `/api/customers/<id>` | Fetch customer details by ID | None | `200`, `404` |
| `GET` | `/api/customers` | List all registered customers | None | `200` |
| `GET` | `/api/products` | List retail product catalog | Optional query: `?category=Electronics` | `200` |
| `POST` | `/api/orders` | Create an order with line items | JSON: `customer_id`, `items: [{product_id, quantity}]` | `201`, `400`, `404`, `409` |
| `GET` | `/api/orders/<id>` | Fetch itemized order details | None | `200`, `404` |
| `PUT` | `/api/orders/<id>/status` | Update order fulfillment status | JSON: `status` (`CONFIRMED`, `SHIPPED`, etc.) | `200`, `400`, `404` |
| `GET` | `/api/orders` | Filter and paginate orders | Query params: `status`, `start_date`, `end_date`, `search`, `page` | `200`, `400` |
| `GET` | `/api/analytics/summary` | Executive analytics & KPI data | None | `200` |

---

## Database Architecture

The relational database model is normalized in Third Normal Form (3NF) with integrity constraints:

```sql
customers (customer_id [PK], first_name, last_name, email [UNIQUE], city, state, country, postal_code, created_at)
products (product_id [PK], sku [UNIQUE], product_name, category, unit_price, stock_quantity, created_at)
orders (order_id [PK], order_number [UNIQUE], customer_id [FK], order_date, status, subtotal, tax_amount, shipping_fee, total_amount, payment_method, shipping_address, created_at, updated_at)
order_items (item_id [PK], order_id [FK], product_id [FK], quantity, unit_price, item_total, created_at)
```

### Key Integrity Constraints & Rules
- **State Machine Constraint**: `status IN ('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')`
- **Quantity Constraint**: `quantity > 0`
- **Pricing Non-Negativity**: `unit_price >= 0`, `subtotal >= 0`, `total_amount >= 0`
- **Referential Integrity**: Cascading delete on order items; restricted deletion on customers with active orders.

---

## AWS Batch Processing Workflow

The AWS Lambda module (`aws/lambda_function.py`) simulates a serverless ingestion pipeline triggered by S3 file uploads:

1. **Header Validation**: Checks for required columns (`order_number`, `customer_id`, `order_date`, `status`, `product_sku`, `quantity`, `unit_price`, `payment_method`).
2. **Data Type & Domain Validation**:
   - `customer_id`: Must be a positive integer.
   - `quantity`: Must be $> 0$.
   - `unit_price`: Must be $\ge 0.00$.
   - `status`: Must match approved enum states.
   - `order_date`: Must parse valid ISO/standard date format (`YYYY-MM-DD`).
3. **Batch Uniqueness**: Identifies and flags duplicate `order_number` values within the batch.
4. **Enrichment**: Computes subtotal, standard tax ($8\%$), shipping ($10.00 if subtotal < $100), and total amount.
5. **Output Routing**: Splits rows into `valid_records` and `rejected_records` (with row number and error reasons).

### Execute AWS Pipeline Simulation
```bash
python aws/simulate_s3_pipeline.py
```

---

## Power BI Dashboard & Data Reconciliation

The Power BI data model establishes a Star Schema linking the 4 normalized tables.

### Reconciliation Summary (PostgreSQL vs Power BI)

| Measure / Metric | PostgreSQL SQL Query | Power BI DAX Formula | PostgreSQL Value | Power BI Value | Variance | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Total Orders** | `SELECT COUNT(*) FROM orders;` | `COUNTROWS('orders')` | 10 | 10 | 0 | **RECONCILED** |
| **Net Revenue** | `SELECT SUM(total_amount) FROM orders WHERE status != 'CANCELLED';` | `CALCULATE(SUM('orders'[total_amount]), 'orders'[status] <> "CANCELLED")` | $2,307.84 | $2,307.84 | $0.00 (0.00%) | **RECONCILED** |
| **Gross Revenue**| `SELECT SUM(total_amount) FROM orders;` | `SUM('orders'[total_amount])` | $2,457.16 | $2,457.16 | $0.00 (0.00%) | **RECONCILED** |
| **Average Order Value** | `SELECT AVG(total_amount) FROM orders WHERE status != 'CANCELLED';` | `DIVIDE([Net Revenue], [Active Orders])` | $256.43 | $256.43 | $0.00 (0.00%) | **RECONCILED** |
| **Delivered Orders** | `SELECT COUNT(*) FROM orders WHERE status = 'DELIVERED';` | `CALCULATE([Total Orders], 'orders'[status] = "DELIVERED")` | 4 | 4 | 0 | **RECONCILED** |

### Run Automated Reconciliation Audit
```bash
python scripts/run_reconciliation.py
```

---

## Testing & Quality Engineering

The test suite covers multiple layers of the testing pyramid:

### 1. Execute All Automated Tests (Pytest)
```bash
pytest -v
```

### 2. Test Execution Breakdown
- **Unit & Business Logic Tests** (`tests/unit/`): 9 tests covering customer validation, order payload parsing, date validation, and status transition rules.
- **REST API Tests** (`tests/api/`): 18 tests covering customer/order endpoints, pagination, status updates, 400 Bad Request, 404 Not Found, and 409 Conflict.
- **Data Quality Tests** (`tests/data_quality/`): 9 tests verifying the 6 Data Quality Pillars and Source-to-Target reconciliation.
- **Playwright UI Tests** (`tests/ui/`): 10 tests verifying authentication, filtering, search, order details, state transitions, and responsive views.
- **AWS Lambda Tests** (`aws/test_lambda.py`): 3 tests verifying clean batch parsing, corrupted batch anomaly rejection, and empty events.

### 3. Generate Formatted Excel Test Execution Report
```bash
python scripts/generate_excel_report.py
```
Outputs: `reports/Retail_Order_Test_Execution_Report.xlsx` containing the Executive Summary, Test Case Log, and Data Quality Matrix.

---

## Defect Management (Jira Log)

Four realistic defects were logged, investigated, and verified:

| Defect ID | Severity | Component | Summary | Status |
| :---: | :---: | :--- | :--- | :---: |
| **RET-101** | Medium | Web UI | Search input parameter was cleared when modifying status dropdown filter. | `CLOSED (VERIFIED)` |
| **RET-102** | High | REST API | PUT `/api/orders/{id}/status` rejected valid lowercase status strings. | `CLOSED (VERIFIED)` |
| **RET-103** | High | Database / Math | Float decimal precision caused $0.01 rounding mismatch in multi-item orders. | `CLOSED (VERIFIED)` |
| **RET-104** | Critical | Power BI | Power BI Net Revenue DAX formula included CANCELLED orders in executive KPI. | `CLOSED (VERIFIED)` |

Detailed reproduction steps, logs, and root cause analysis are documented in `defects/DEFECTS_LOG.md`.

---

## What I Learned

- **Quality Engineering Beyond UI**: Realized that testing APIs and data integrity at the database and ETL levels catches defects earlier and cheaper than UI-only testing.
- **Data Quality Pillars**: Applied the 6 core pillars of Data Quality (Completeness, Accuracy, Consistency, Uniqueness, Validity, Timeliness) using automated SQL checks.
- **Reconciliation Rigor**: Learned how simple formula discrepancies (e.g., handling cancelled orders in DAX vs SQL) can distort executive metrics if cross-system reconciliation is not automated.
- **Playwright Test Isolation**: Designed isolated browser contexts per test to eliminate flaky authentication test bleed across test fixtures.
- **Defect Lifecycle Discipline**: Practiced writing clear, reproducible defect reports with exact steps, root causes, and verification criteria.

---

## Author

- **Harsha Raju**
- Quality Engineering Portfolio Project
- GitHub Repository: [Retail-Order-Analytics-and-Quality-Engineering-Platform](https://github.com/harsharaju1314-hash/Retail-Order-Analytics-and-Quality-Engineering-Platform)
