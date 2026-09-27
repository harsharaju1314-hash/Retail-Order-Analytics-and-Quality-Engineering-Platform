# Security, Negative & Boundary Test Cases
## Project: Retail Order Analytics & Quality Engineering Platform

---

### Test Suite: Security & Negative Boundary Checks

| Test ID | Test Scenario | Input / Attack Vector | Expected System Behavior | Status |
| :--- | :--- | :--- | :--- | :---: |
| `TC-SEC-001` | SQL Injection via Search Input | Input `' OR '1'='1` in search field | Query parameterized; returns 0 matches or literal match; no SQL syntax error. | PASS |
| `TC-SEC-002` | XSS Payload in Customer Name | `<script>alert('xss')</script>` in `first_name` | Escaped by Jinja2 / JSON serializer; raw script is not executed. | PASS |
| `TC-BND-001` | Maximum Quantity Boundary | `quantity = 1000` | Order processed or capped per inventory limits; no arithmetic overflow. | PASS |
| `TC-BND-002` | Zero and Negative Quantity | `quantity = 0`, `quantity = -5` | Rejected with HTTP 400 Bad Request. | PASS |
| `TC-BND-003` | Price Boundary Check | `unit_price = 0.00` (Free item) | Accepted if promotional, calculated as $0.00 without division errors. | PASS |
| `TC-BND-004` | Malformed JSON Payload | Unclosed curly brace `{"customer_id": 1` | Server rejects with HTTP 400 Bad Request; server does not crash. | PASS |
| `TC-BND-005` | Large Text Input Buffer | 10,000 character shipping address | Validated or safely truncated; database constraint protects buffer. | PASS |
