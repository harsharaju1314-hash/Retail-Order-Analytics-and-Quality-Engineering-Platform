# Playwright UI Automation Test Cases
## Project: Retail Order Analytics & Quality Engineering Platform

---

### Test Suite: Playwright UI End-to-End Automation

| Test ID | Test Scenario | Automation Tool | Steps & Assertions | Status |
| :--- | :--- | :---: | :--- | :---: |
| `TC-UI-001` | Valid Login Flow | Playwright / Chromium | 1. Navigate to `/login`<br>2. Enter `admin@retail.com` and `Admin123!`<br>3. Click Sign In<br>4. Assert URL is `/orders` and navbar displays username. | PASS |
| `TC-UI-002` | Invalid Login Flow | Playwright / Chromium | 1. Navigate to `/login`<br>2. Enter invalid password<br>3. Click Sign In<br>4. Assert error alert `#login-error-alert` is visible. | PASS |
| `TC-UI-003` | Order Search by Customer / Order # | Playwright / Chromium | 1. Login to portal<br>2. Input "Alice" in `#search-input`<br>3. Submit filter<br>4. Assert visible rows contain "Alice". | PASS |
| `TC-UI-004` | Order Status Filtering | Playwright / Chromium | 1. Select `DELIVERED` from `#status-select`<br>2. Submit filter<br>3. Assert every rendered status badge contains "DELIVERED". | PASS |
| `TC-UI-005` | Date Range Filtering | Playwright / Chromium | 1. Set `#start-date` and `#end-date`<br>2. Submit filter<br>3. Verify filtered table row count matches date boundaries. | PASS |
| `TC-UI-006` | View Order Details & Line Items | Playwright / Chromium | 1. Click "View" button on Order 1<br>2. Assert `#order-title` contains order number<br>3. Assert `#order-items-table` contains correct line items. | PASS |
| `TC-UI-007` | Order Status Transition via UI | Playwright / Chromium | 1. Navigate to Order Detail<br>2. Select `CONFIRMED` in `#new-status-select`<br>3. Click update button<br>4. Assert `#current-status-badge` reflects `CONFIRMED`. | PASS |
| `TC-UI-008` | Empty Search State Feedback | Playwright / Chromium | 1. Search for non-existent term `XYZ-NON-EXISTENT`<br>2. Assert `#no-orders-msg` container is visible. | PASS |
| `TC-UI-009` | Interactive Order Creation Flow | Playwright / Chromium | 1. Navigate to `/create-order`<br>2. Select customer and product<br>3. Submit order<br>4. Assert redirection to newly created order detail page. | PASS |
| `TC-UI-010` | Analytics Page KPIs Display | Playwright / Chromium | 1. Navigate to `/analytics`<br>2. Verify KPI cards (`#kpi-total-orders`, `#kpi-total-revenue`) load values. | PASS |
