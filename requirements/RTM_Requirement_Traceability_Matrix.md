# Requirement Traceability Matrix (RTM)
## Project: Retail Order Analytics & Quality Engineering Platform

The Requirement Traceability Matrix (RTM) maps business and functional requirements to corresponding test cases, test types, expected outcomes, actual execution results, and associated defect logs.

---

| Req ID | Requirement Description | Test Case ID | Test Type | Expected Result | Actual Result | Status | Defect ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **FR-101.1** | Customer profile creation with mandatory fields | `TC-API-CUST-001` | API Testing | Returns 201 Created and customer JSON payload | HTTP 201 Created with JSON structure | `PASS` | - |
| **FR-101.1** | Reject customer payload missing mandatory fields | `TC-API-CUST-002` | Negative / API | Returns 400 Bad Request with missing field name | HTTP 400 with `{'field': 'email'}` | `PASS` | - |
| **FR-101.2** | Reject customer creation with duplicate email | `TC-API-CUST-003` | Boundary / API | Returns 409 Conflict with duplicate email warning | HTTP 409 Conflict with descriptive error | `PASS` | - |
| **FR-101.2** | Reject customer creation with invalid email syntax | `TC-API-CUST-004` | Negative / API | Returns 400 Bad Request for malformed email | HTTP 400 with invalid format error | `PASS` | - |
| **FR-102.1** | Place order with valid customer and products | `TC-API-ORD-001` | Functional / API | Returns 201 Created with calculated subtotal, tax, total | HTTP 201 Created with calculated amounts | `PASS` | - |
| **FR-102.1** | Reject order referencing non-existent customer ID | `TC-API-ORD-002` | Negative / API | Returns 404 Not Found (`Customer not found`) | HTTP 404 Not Found returned | `PASS` | - |
| **FR-102.1** | Reject order referencing non-existent product ID | `TC-API-ORD-003` | Negative / API | Returns 404 Not Found (`Product not found`) | HTTP 404 Not Found returned | `PASS` | - |
| **FR-102.2** | Reject order with non-positive item quantity ($\le 0$) | `TC-API-ORD-004` | Boundary / API | Returns 400 Bad Request for zero or negative quantity | HTTP 400 Bad Request | `PASS` | - |
| **FR-102.3** | Verify financial calculations (subtotal, 8% tax, shipping) | `TC-UNIT-FIN-001` | Unit / Data | Line items match subtotal; tax is 8%; shipping rules apply | Math verified with exact precision | `PASS` | - |
| **FR-103.1** | Order creation defaults to PENDING status | `TC-API-ORD-005` | Functional / API | Newly created order status equals 'PENDING' | Status = 'PENDING' | `PASS` | - |
| **FR-103.2** | Valid status transition: PENDING to CONFIRMED | `TC-API-STAT-001` | Integration / API | Returns 200 OK and status updated to CONFIRMED | HTTP 200 OK, status updated | `PASS` | - |
| **FR-103.3** | Reject invalid status transition (DELIVERED to PENDING) | `TC-API-STAT-002` | Negative / API | Returns 400 Bad Request with transition violation | HTTP 400 Bad Request | `PASS` | - |
| **FR-104.1** | Search orders by customer name / order number | `TC-UI-SEARCH-001` | Playwright UI | Table filters rows matching search term dynamically | Table shows filtered matching orders | `PASS` | - |
| **FR-104.2** | Filter orders by status dropdown | `TC-UI-FILTER-001` | Playwright UI | Table only displays orders matching selected status | Orders filtered by status | `PASS` | - |
| **FR-104.2** | Filter orders by date range | `TC-UI-FILTER-002` | Playwright UI | Table displays orders within date boundary | Orders within date range displayed | `PASS` | - |
| **FR-105.1** | AWS Lambda batch ingestion of valid CSV | `TC-AWS-LAMBDA-001`| Data Pipeline | Ingests 5 rows, validates 5 rows, 100% pass rate | 5 valid rows ingested & enriched | `PASS` | - |
| **FR-105.2** | AWS Lambda rejection of corrupted CSV records | `TC-AWS-LAMBDA-002`| Data Quality | Rejects rows with missing fields, bad dates, bad statuses | 5 rejected rows logged with reasons | `PASS` | - |
| **FR-106.1** | SQL Data Completeness & Uniqueness Validation | `TC-SQL-DQ-001` | SQL / Data Quality | No duplicate order numbers, no orphan line items | Verified 0 duplicates, 0 orphans | `PASS` | - |
| **FR-106.2** | Source-to-Target Reconciliation (PostgreSQL vs Power BI) | `TC-BI-RECON-001` | BI Reconciliation | SQL aggregations match Power BI DAX measures 100% | 0.00% variance across all KPIs | `PASS` | - |

---

### Quality Summary Metrics
- **Total Test Cases Mapped:** 18
- **Passed:** 18
- **Failed:** 0 (Active Defect Fix Verification Complete)
- **Requirements Coverage:** 100%
