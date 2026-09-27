# Defects & Bug Management Log (Jira Format)
## Project: Retail Order Analytics & Quality Engineering Platform

---

### Defect 1: UI Defect (RET-101)
- **Defect ID:** `RET-101`
- **Title:** Order Search Input Cleared When Modifying Status Filter Dropdown
- **Component:** Web UI / Frontend Filters
- **Severity:** Medium
- **Priority:** P3 - Medium
- **Reported By:** Quality Engineer
- **Assigned To:** Frontend Developer
- **Status:** `CLOSED (VERIFIED)`
- **Environment:** Chrome / Chromium (Playwright Test Runner)
- **Description:** When a user types a search term (e.g., "Alice") into the search box and then changes the status filter dropdown without pressing the filter button, the search input was wiped out upon form auto-submission.
- **Steps to Reproduce:**
  1. Navigate to `/orders`.
  2. Type "Alice" into `#search-input`.
  3. Select `DELIVERED` from `#status-select`.
  4. Click `Filter`.
- **Expected Result:** Table should display orders matching customer "Alice" AND status "DELIVERED".
- **Actual Result:** Search query parameter was ignored, displaying all `DELIVERED` orders across all customers.
- **Root Cause:** Filter form action did not bind query parameters across combined GET parameters.
- **Fix / Resolution:** Updated form input binding to preserve active search parameters alongside status selection. Verified by test `TC-UI-004`.

---

### Defect 2: API Defect (RET-102)
- **Defect ID:** `RET-102`
- **Title:** PUT `/api/orders/{id}/status` Rejects Valid Lowercase Status String
- **Component:** REST API / Order Service
- **Severity:** High
- **Priority:** P2 - High
- **Reported By:** Quality Engineer
- **Assigned To:** Backend Developer
- **Status:** `CLOSED (VERIFIED)`
- **Environment:** REST API Test Harness
- **Description:** Sending `{"status": "confirmed"}` (lowercase) in the request body returned `HTTP 400 Bad Request` claiming invalid status, instead of normalizing case before transition validation.
- **Steps to Reproduce:**
  1. Create order in `PENDING` status.
  2. Send PUT `/api/orders/1/status` with payload `{"status": "confirmed"}`.
- **Expected Result:** API normalizes string to `CONFIRMED` and returns `HTTP 200 OK`.
- **Actual Result:** API returned `HTTP 400 Bad Request`: `"Invalid status 'confirmed'"`.
- **Root Cause:** `validate_status_transition` was performing set membership check prior to executing `.upper()`.
- **Fix / Resolution:** Added case normalization `.strip().upper()` at input entry point before transition evaluation. Verified by test `TC-API-014`.

---

### Defect 3: Data Quality Discrepancy (RET-103)
- **Defect ID:** `RET-103`
- **Title:** Order Subtotal Calculation Discrepancy on Floating-Point Decimal Precision
- **Component:** Database / Order Engine
- **Severity:** High
- **Priority:** P2 - High
- **Reported By:** Data Quality Engineer
- **Assigned To:** Database / Data Engineer
- **Status:** `CLOSED (VERIFIED)`
- **Environment:** PostgreSQL / SQL Test Suite
- **Description:** Line items calculated with IEEE 754 float types accumulated a $0.01 fractional rounding error against recorded order header subtotal.
- **Steps to Reproduce:**
  1. Execute `sql-validation/accuracy_checks.sql` (Check 2).
  2. Observe query results for orders with fractional tax rates.
- **Expected Result:** Discrepancy between header subtotal and sum of item totals = $0.00.
- **Actual Result:** Discrepancy of $0.01 flagged by automated SQL accuracy check.
- **Root Cause:** Standard Python `float` was used instead of Python `decimal.Decimal` and PostgreSQL `NUMERIC(10,2)` types.
- **Fix / Resolution:** Migrated database columns to `NUMERIC(10,2)` and applied explicit `Decimal.quantize(Decimal('0.01'))` rounding in API service layer.

---

### Defect 4: Dashboard Reconciliation Mismatch (RET-104)
- **Defect ID:** `RET-104`
- **Title:** Power BI Net Revenue KPI Overstated Due to Inclusion of CANCELLED Orders
- **Component:** Power BI Dashboard / DAX Measures
- **Severity:** High
- **Priority:** P1 - Critical
- **Reported By:** BI Quality Engineer
- **Assigned To:** BI Developer
- **Status:** `CLOSED (VERIFIED)`
- **Environment:** Power BI Desktop / PostgreSQL
- **Description:** The executive "Net Revenue" KPI card in Power BI was displaying $2,266.05 while the PostgreSQL reconciliation query reported active revenue as $2,116.73 (a variance of $149.32).
- **Steps to Reproduce:**
  1. Open Power BI Dashboard report.
  2. Inspect "Net Revenue" KPI visual.
  3. Execute SQL query: `SELECT SUM(total_amount) FROM orders WHERE status != 'CANCELLED';`.
- **Expected Result:** Power BI Net Revenue = $2,116.73.
- **Actual Result:** Power BI Net Revenue = $2,266.05 (included Order 7 which is CANCELLED).
- **Root Cause:** DAX formula used unconditional `SUM('orders'[total_amount])` instead of filtering out `status <> "CANCELLED"`.
- **Fix / Resolution:** Updated DAX measure to:
  `Net Revenue = CALCULATE(SUM('orders'[total_amount]), 'orders'[status] <> "CANCELLED")`.
  Executed SQL reconciliation query to confirm $0.00 variance.
