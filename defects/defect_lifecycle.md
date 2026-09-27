# Defect Management & Triage Lifecycle
## Project: Retail Order Analytics & Quality Engineering Platform

---

### 1. Defect Workflow States

```
  +-----------+       Triage & Assign       +-------------+
  |  NEW /    |  ------------------------>  | IN PROGRESS |
  | SUBMITTED |                             +-------------+
  +-----------+                                    |
        |                                          | Code Fix
        | Invalid / Dup                            v
        v                                   +-------------+
  +-----------+                             |  RESOLVED   |
  |  REJECTED |                             +-------------+
  +-----------+                                    |
                                                   | Deploy & QA Retest
                                                   v
  +-----------+          QA Passed          +-------------+
  |  CLOSED   |  <------------------------  |  READY FOR  |
  | (VERIFIED)|                             |     QA      |
  +-----------+                             +-------------+
        ^                                          |
        |           Failed Retest                  |
        +------------------------------------------+
                    (Re-open to In Progress)
```

---

### 2. Severity and Priority Matrix

| Level | Severity (Technical Impact) | Priority (Business Urgency) | SLA Target |
| :--- | :--- | :--- | :--- |
| **P1 / Critical** | Complete data corruption, financial misstatement in BI, critical API outage. | Fix immediately, block release. | < 4 hours |
| **P2 / High** | Core API validation failure, data accuracy mismatch, state machine breakdown. | Fix in active sprint. | < 24 hours |
| **P3 / Medium** | UI filter glitch, layout anomaly, non-blocking edge case. | Schedule for next sprint. | < 3 days |
| **P4 / Low** | Cosmetic typography, minor styling, documentation typo. | Low priority backlog. | When feasible |

---

### 3. Defect Reporting Standards
Every logged defect must contain:
1. **Defect ID** (e.g. `RET-101`)
2. **Clear Summary**
3. **Environment Details** (OS, browser version, DB version, test runner)
4. **Step-by-Step Reproduction Instructions**
5. **Expected vs. Actual Result**
6. **Log Traces / SQL Query Evidence / Screen Capture Evidence**
7. **Severity & Priority Classification**
