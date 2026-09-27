# REST API Test Cases & Specifications
## Project: Retail Order Analytics & Quality Engineering Platform

---

### Test Suite: Customer REST APIs

| Test ID | Endpoint | Method | Scenario | Payload / Params | Expected Status | Expected Assertion | Status |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| `TC-API-001` | `/api/customers` | POST | Create valid customer | Valid customer JSON | `201 Created` | `message` = success, `customer.customer_id` is int | PASS |
| `TC-API-002` | `/api/customers` | POST | Missing mandatory email | `{ "first_name": "Sam", "last_name": "T" }` | `400 Bad Request` | `error` mentions email | PASS |
| `TC-API-003` | `/api/customers` | POST | Duplicate customer email | Existing email payload | `409 Conflict` | `error` contains duplicate email | PASS |
| `TC-API-004` | `/api/customers/1` | GET | Retrieve customer by ID | ID = 1 | `200 OK` | `customer_id` == 1, email present | PASS |
| `TC-API-005` | `/api/customers/9999`| GET | Non-existent customer | ID = 9999 | `404 Not Found` | `error` = customer not found | PASS |
| `TC-API-006` | `/api/customers` | GET | List all customers | None | `200 OK` | `total` >= 1, `customers` is array | PASS |

---

### Test Suite: Order REST APIs

| Test ID | Endpoint | Method | Scenario | Payload / Params | Expected Status | Expected Assertion | Status |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| `TC-API-007` | `/api/orders` | POST | Create valid order | Valid order + items | `201 Created` | `order.order_number` present, status = PENDING | PASS |
| `TC-API-008` | `/api/orders` | POST | Non-existent customer | `customer_id: 8888` | `404 Not Found` | `error` = customer not found | PASS |
| `TC-API-009` | `/api/orders` | POST | Non-existent product | `product_id: 8888` | `404 Not Found` | `error` = product not found | PASS |
| `TC-API-010` | `/api/orders` | POST | Invalid quantity zero | `quantity: 0` | `400 Bad Request` | `error` = quantity must be > 0 | PASS |
| `TC-API-011` | `/api/orders` | POST | Empty payload | `{}` | `400 Bad Request` | `error` = empty request | PASS |
| `TC-API-012` | `/api/orders/1` | GET | Get order with items | ID = 1 | `200 OK` | `items` array has elements, financial totals | PASS |
| `TC-API-013` | `/api/orders/9999` | GET | Non-existent order | ID = 9999 | `404 Not Found` | `error` = order not found | PASS |
| `TC-API-014` | `/api/orders/1/status`| PUT | Valid transition | `{"status": "CONFIRMED"}` | `200 OK` | `order.status` == CONFIRMED | PASS |
| `TC-API-015` | `/api/orders/1/status`| PUT | Invalid status string | `{"status": "IN_FLIGHT"}` | `400 Bad Request` | `error` = invalid status | PASS |
| `TC-API-016` | `/api/orders` | GET | Filter by status | `?status=DELIVERED` | `200 OK` | All returned orders have status DELIVERED | PASS |
| `TC-API-017` | `/api/orders` | GET | Filter by date range | `?start_date=2026-02-01` | `200 OK` | All orders >= 2026-02-01 | PASS |
| `TC-API-018` | `/api/analytics/summary`| GET| Reconciled Analytics | None | `200 OK` | `kpis.total_orders`, `kpis.total_revenue` present | PASS |
