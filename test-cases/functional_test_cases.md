# Functional & System Test Cases
## Project: Retail Order Analytics & Quality Engineering Platform

---

### TC-FUNC-001: Customer Profile Onboarding
- **Module:** Customer Management
- **Type:** Positive Functional Test
- **Preconditions:** Server and Database running.
- **Steps:**
  1. Prepare valid payload with `first_name='John'`, `last_name='Doe'`, `email='john.doe@test.com'`, `city='Dallas'`, `state='TX'`.
  2. Send POST request to `/api/customers`.
  3. Validate response code is 201 Created.
  4. Query database to verify record insertion in `customers` table.
- **Expected Result:** Customer is persisted with unique `customer_id` and correct timestamps.
- **Status:** PASS

---

### TC-FUNC-002: Multi-Item Order Creation & Pricing Precision
- **Module:** Order Engine
- **Type:** Positive Functional Test
- **Preconditions:** Customer ID 1 and Product IDs 1, 2 exist.
- **Steps:**
  1. Send POST request to `/api/orders` with Product 1 (Qty: 2 @ $149.99 = $299.98) and Product 2 (Qty: 1 @ $89.50 = $89.50).
  2. Verify Subtotal = $389.48.
  3. Verify Tax (8%) = $31.16.
  4. Verify Shipping = $0.00 (Subtotal >= $100).
  5. Verify Total = $420.64.
- **Expected Result:** Order is created in `PENDING` state with accurate financial calculations and order item linkages.
- **Status:** PASS

---

### TC-FUNC-003: Order Fulfillment Lifecycle State Progression
- **Module:** Order Workflow
- **Type:** State Machine Functional Test
- **Preconditions:** Order in `PENDING` status.
- **Steps:**
  1. Transition `PENDING` $\rightarrow$ `CONFIRMED`. Expect 200 OK.
  2. Transition `CONFIRMED` $\rightarrow$ `SHIPPED`. Expect 200 OK.
  3. Transition `SHIPPED` $\rightarrow$ `DELIVERED`. Expect 200 OK.
  4. Attempt transition `DELIVERED` $\rightarrow$ `PENDING`. Expect 400 Bad Request.
- **Expected Result:** Allowed transitions succeed; terminal state transitions are blocked with business validation errors.
- **Status:** PASS

---

### TC-FUNC-004: Cancellation from Pending and Confirmed States
- **Module:** Order Workflow
- **Type:** Business Rule Functional Test
- **Steps:**
  1. Create order in `PENDING` status.
  2. Send PUT request to update status to `CANCELLED`. Expect 200 OK.
  3. Create order and move to `CONFIRMED`.
  4. Update status to `CANCELLED`. Expect 200 OK.
- **Expected Result:** Orders can be cancelled from PENDING and CONFIRMED stages.
- **Status:** PASS
