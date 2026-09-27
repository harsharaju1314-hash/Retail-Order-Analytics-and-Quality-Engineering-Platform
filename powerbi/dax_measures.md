# Power BI DAX Measures & Formulas
## Project: Retail Order Analytics Platform

---

### 1. Total Orders
```dax
Total Orders = COUNTROWS('orders')
```
*Description:* Counts total volume of order records in the fact table.

---

### 2. Active Orders
```dax
Active Orders = CALCULATE(
    COUNTROWS('orders'),
    'orders'[status] <> "CANCELLED"
)
```
*Description:* Total orders excluding cancelled records.

---

### 3. Gross Revenue
```dax
Gross Revenue = SUM('orders'[total_amount])
```
*Description:* Aggregate sum of all order totals ($2,266.05).

---

### 4. Net Revenue (Executive KPI)
```dax
Net Revenue = CALCULATE(
    SUM('orders'[total_amount]),
    'orders'[status] <> "CANCELLED"
)
```
*Description:* Total recognized revenue from active/fulfilled orders ($2,116.73).

---

### 5. Average Order Value (AOV)
```dax
Average Order Value = DIVIDE(
    [Net Revenue],
    [Active Orders],
    0
)
```
*Description:* Average revenue per non-cancelled transaction ($235.19).

---

### 6. Delivered Order Rate (%)
```dax
Delivered Order Rate = DIVIDE(
    CALCULATE(COUNTROWS('orders'), 'orders'[status] = "DELIVERED"),
    [Total Orders],
    0
) * 100
```
*Description:* Proportion of orders successfully delivered to customers.

---

### 7. Total Units Sold
```dax
Total Units Sold = SUM('order_items'[quantity])
```
*Description:* Total physical product count ordered across all line items.
