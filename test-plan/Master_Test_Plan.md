# Master Test Plan
## Project: Retail Order Analytics & Quality Engineering Platform

---

### 1. Introduction & Overview
This Master Test Plan defines the test strategy, execution scope, environments, automated tooling, quality gates, and risk management approach for the **Retail Order Analytics & Quality Engineering Platform**.

The quality engineering scope encompasses:
- REST API functional and contract testing
- UI browser automation and workflow validation
- Data pipeline validation (AWS S3 $\rightarrow$ AWS Lambda)
- SQL Data Quality checks (Completeness, Accuracy, Consistency, Uniqueness, Validity, Timeliness)
- Source-to-Target BI reconciliation between transactional database and analytical dashboard.

---

### 2. Scope of Testing

#### 2.1 In-Scope
- **Functional Testing**: Verification of customer creation, order placement, lifecycle state progression.
- **API Testing**: Status code validation (200, 201, 400, 404, 409), schema validation, header checks, payload validation.
- **UI Automation**: Playwright automated tests covering authentication, search, filtering, order detail inspection, and status modifications.
- **Data Quality & ETL Validation**: Automated SQL integrity checks, AWS Lambda batch parsing, schema enforcement.
- **BI Reconciliation**: Cross-system verification between PostgreSQL tables and Power BI DAX KPIs.
- **Negative & Boundary Testing**: Testing zero quantities, negative prices, duplicate keys, SQL injection resilience, and malformed JSON payloads.

#### 2.2 Out-of-Scope
- Distributed load and stress testing exceeding 10,000 req/sec.
- Multi-region failover and disaster recovery drills.

---

### 3. Test Strategy & Levels

```
+-------------------------------------------------------------+
|                 Power BI Visual Reconciliation               |
+-------------------------------------------------------------+
|              Playwright UI End-to-End Automation             |
+-------------------------------------------------------------+
|               Postman & Pytest REST API Testing              |
+-------------------------------------------------------------+
|            SQL Data Quality (6 Core Data Quality Pillars)   |
+-------------------------------------------------------------+
|             Unit & Business Logic Rule Validation            |
+-------------------------------------------------------------+
```

---

### 4. Environments & Tooling

| Category | Tool / Framework | Version / Configuration |
| :--- | :--- | :--- |
| **Test Automation Framework** | Pytest | 8.x / 9.x |
| **UI Automation Tool** | Playwright (Python) | 1.40+ (Chromium) |
| **API Testing** | Postman / Requests / Pytest | Collection v2.1 |
| **Database** | PostgreSQL / SQLite (Test Harness) | Relational SQL |
| **Data Processing** | AWS S3 / AWS Lambda (Python Handler) | Serverless Data Pipeline |
| **BI & Analytics** | Power BI Desktop / Service | Tabular Model / DAX |
| **Test Management & Execution** | Microsoft Excel / Markdown | Formatted Execution Sheets |
| **Defect Tracking** | Jira Software | Scrum / Bug Tracking Workflow |
| **CI/CD Automation** | GitHub Actions | Ubuntu / Python Runner |

---

### 5. Entry & Exit Criteria

#### 5.1 Entry Criteria
1. Database schema generated and seed datasets initialized.
2. Flask API and web server running and accessible.
3. Test datasets and corrupted batch test files prepared.
4. Test suites (Unit, API, Data Quality, UI) configured in Pytest.

#### 5.2 Exit Criteria
1. 100% execution of all automated test suites.
2. 0 Critical (Blocker) or High severity open defects.
3. All data quality validation queries execute with 0 unresolved integrity anomalies.
4. Source-to-Target reconciliation matches with $0.00\%$ discrepancy.
5. GitHub Actions CI pipeline passes cleanly on main branch.
