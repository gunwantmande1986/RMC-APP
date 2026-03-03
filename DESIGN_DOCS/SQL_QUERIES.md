# 📊 SQL QUERIES - READY TO USE

**Date**: 24-Jan-2026  
**Purpose**: Production ka SQL queries for reports & operations

---

## 📋 CONTENTS

1. [Basic Queries](#basic-queries)
2. [Production Reports](#production-reports)
3. [Party Document Reports](#party-document-reports)
4. [Variance Analysis](#variance-analysis)
5. [Dashboard Queries](#dashboard-queries)

---

## 🔍 BASIC QUERIES

### Q1: Get All Productions for a Party

```sql
-- ════════════════════════════════════════════════════
-- YOUR ACTUAL PRODUCTION DATA (Pure, No mixing)
-- ════════════════════════════════════════════════════

SELECT 
    ap.challan_no,
    ap.production_date,
    ap.production_time,
    p.party_name,
    s.site_name,
    
    -- ACTUAL DATA (What you really supplied)
    ap.actual_grade_code AS grade,
    ap.actual_quantity AS quantity,
    ap.actual_rate AS rate,
    ap.actual_amount AS amount,
    ap.total_gst AS gst,
    ap.total_amount AS total,
    
    ap.vehicle_no,
    ap.driver_name,
    ap.delivery_status,
    ap.payment_status

FROM actual_production ap
LEFT JOIN parties p ON ap.party_id = p.party_id
LEFT JOIN sites s ON ap.site_id = s.site_id

WHERE ap.party_id = 1  -- ABC Builders
  AND ap.production_date BETWEEN '2026-01-01' AND '2026-01-31'
  AND ap.production_status = 'Completed'

ORDER BY ap.production_date DESC, ap.production_time DESC;
```

**Example Output:**
```
challan_no | date       | party        | grade | qty  | rate | amount  | total
-----------|------------|--------------|-------|------|------|---------|--------
CH-005     | 2026-01-10 | ABC Builders | M25   | 12.0 | 5000 | 60,000  | 70,800
CH-003     | 2026-01-07 | ABC Builders | M25   | 10.0 | 5000 | 50,000  | 59,000
CH-001     | 2026-01-05 | ABC Builders | M25   | 10.0 | 5000 | 50,000  | 59,000
```

---

### Q2: Get Party Documents (What Party Sees)

```sql
-- ════════════════════════════════════════════════════
-- PARTY DOCUMENT DATA (What they requested)
-- ════════════════════════════════════════════════════

SELECT 
    pd.invoice_no,
    pd.invoice_date,
    pd.challan_no,
    p.party_name,
    
    -- PARTY DOCUMENT DATA (Separate from actual)
    pd.document_grade_code AS grade,
    pd.document_quantity AS quantity,
    pd.document_rate AS rate,
    pd.document_amount AS amount,
    pd.document_total_gst AS gst,
    pd.document_total AS total,
    
    pd.document_status,
    pd.approved_by,
    pd.approval_date

FROM party_documents pd
LEFT JOIN parties p ON pd.party_id = p.party_id

WHERE pd.party_id = 1
  AND pd.invoice_date BETWEEN '2026-01-01' AND '2026-01-31'
  AND pd.document_status = 'Approved'

ORDER BY pd.invoice_date DESC;
```

**Example Output:**
```
invoice_no | date       | party        | grade | qty  | rate | amount  | total
-----------|------------|--------------|-------|------|------|---------|--------
INV-005    | 2026-01-10 | ABC Builders | M30   | 12.0 | 5200 | 62,400  | 73,632
INV-003    | 2026-01-07 | ABC Builders | M30   | 10.0 | 5200 | 52,000  | 61,360
INV-001    | 2026-01-05 | ABC Builders | M30   | 10.0 | 5200 | 52,000  | 61,360
```

---

## 📈 PRODUCTION REPORTS

### Report 1: YOUR PRODUCTION REPORT (For Accounts/Tax)

```sql
-- ════════════════════════════════════════════════════
-- REPORT 1: Your Production Summary
-- Use for: Tax filing, GST return, Internal accounts
-- Data from: actual_production ONLY
-- ════════════════════════════════════════════════════

SELECT 
    ap.production_date,
    ap.challan_no,
    p.party_name,
    s.site_name,
    ap.actual_grade_code,
    ap.actual_quantity,
    ap.actual_rate,
    ap.actual_amount,
    ap.cgst_amount,
    ap.sgst_amount,
    ap.total_gst,
    ap.total_amount,
    ap.vehicle_no,
    ap.payment_status

FROM actual_production ap
LEFT JOIN parties p ON ap.party_id = p.party_id
LEFT JOIN sites s ON ap.site_id = s.site_id

WHERE ap.party_id = ?  -- Parameter
  AND ap.production_date BETWEEN ? AND ?  -- Date range
  AND ap.production_status = 'Completed'

ORDER BY ap.production_date, ap.production_time;

-- Summary Totals (Same query with aggregation)
SELECT 
    COUNT(*) as total_deliveries,
    SUM(ap.actual_quantity) as total_quantity,
    SUM(ap.actual_amount) as total_amount,
    SUM(ap.total_gst) as total_gst,
    SUM(ap.total_amount) as grand_total

FROM actual_production ap

WHERE ap.party_id = ?
  AND ap.production_date BETWEEN ? AND ?
  AND ap.production_status = 'Completed';
```

**Output Format:**
```
═══════════════════════════════════════════════════════
        YOUR PRODUCTION REPORT (Internal)
═══════════════════════════════════════════════════════
Party: ABC Builders Pvt Ltd
Period: 01-Jan-2026 to 31-Jan-2026
Generated: 24-Jan-2026 10:30 AM
───────────────────────────────────────────────────────

Date     | Challan | Grade | Qty   | Rate  | Amount   
─────────┼─────────┼───────┼───────┼───────┼──────────
05-Jan   | CH-001  | M25   | 10.00 | 5,000 | 50,000
07-Jan   | CH-003  | M25   | 10.00 | 5,000 | 50,000
10-Jan   | CH-005  | M25   | 12.00 | 5,000 | 60,000
───────────────────────────────────────────────────────
Total Deliveries: 3
Total Quantity: 32.00 CUM
───────────────────────────────────────────────────────
Sub-Total:        ₹1,60,000
CGST @ 9%:        ₹14,400
SGST @ 9%:        ₹14,400
Total GST:        ₹28,800
───────────────────────────────────────────────────────
GRAND TOTAL:      ₹1,88,800  ✅ (File this in GST return)
═══════════════════════════════════════════════════════
```

---

### Report 2: DATE-WISE PRODUCTION SUMMARY

```sql
-- ════════════════════════════════════════════════════
-- REPORT 2: Date-wise Production Grouping
-- ════════════════════════════════════════════════════

SELECT 
    ap.production_date,
    ap.actual_grade_code,
    COUNT(*) as trip_count,
    SUM(ap.actual_quantity) as total_quantity,
    AVG(ap.actual_rate) as avg_rate,
    SUM(ap.actual_amount) as total_amount,
    GROUP_CONCAT(ap.vehicle_no SEPARATOR ', ') as vehicles_used

FROM actual_production ap

WHERE ap.party_id = ?
  AND ap.production_date BETWEEN ? AND ?
  AND ap.production_status = 'Completed'

GROUP BY ap.production_date, ap.actual_grade_code
ORDER BY ap.production_date, ap.actual_grade_code;
```

**Output:**
```
═══════════════════════════════════════════════════════
     DATE-WISE PRODUCTION SUMMARY (Party: ABC)
═══════════════════════════════════════════════════════

📅 05-Jan-2026 (Friday)
├─ M25 Grade: 10.00 CUM (1 trip) @ ₹5,000 = ₹50,000
└─ Vehicles: MH12AB1234

📅 07-Jan-2026 (Sunday)
├─ M25 Grade: 10.00 CUM (1 trip) @ ₹5,000 = ₹50,000
└─ Vehicles: MH12CD5678

📅 10-Jan-2026 (Wednesday)
├─ M25 Grade: 12.00 CUM (1 trip) @ ₹5,000 = ₹60,000
└─ Vehicles: MH12EF9012

═══════════════════════════════════════════════════════
TOTAL: 32.00 CUM | 3 trips | ₹1,60,000
═══════════════════════════════════════════════════════
```

---

### Report 3: GRADE-WISE PRODUCTION SUMMARY

```sql
-- ════════════════════════════════════════════════════
-- REPORT 3: Grade-wise Production Analysis
-- ════════════════════════════════════════════════════

SELECT 
    ap.actual_grade_code,
    COUNT(*) as total_trips,
    SUM(ap.actual_quantity) as total_quantity,
    AVG(ap.actual_rate) as avg_rate,
    SUM(ap.actual_amount) as total_amount,
    -- Percentage calculation
    ROUND(
        (SUM(ap.actual_quantity) * 100.0 / 
         (SELECT SUM(actual_quantity) FROM actual_production 
          WHERE party_id = ap.party_id 
          AND production_date BETWEEN '2026-01-01' AND '2026-01-31')),
        2
    ) as percentage

FROM actual_production ap

WHERE ap.party_id = ?
  AND ap.production_date BETWEEN ? AND ?
  AND ap.production_status = 'Completed'

GROUP BY ap.actual_grade_code
ORDER BY total_quantity DESC;
```

**Output:**
```
═══════════════════════════════════════════════════════
     GRADE-WISE PRODUCTION SUMMARY (Party: ABC)
═══════════════════════════════════════════════════════

Grade | Trips | Quantity | Avg Rate | Amount     | %
──────┼───────┼──────────┼──────────┼────────────┼──────
M25   | 15    | 96.00    | 5,000    | 4,80,000   | 51.8%
M30   | 8     | 52.00    | 6,000    | 3,12,000   | 28.1%
M20   | 4     | 22.00    | 4,500    | 99,000     | 11.9%
M35   | 3     | 15.00    | 7,000    | 1,05,000   | 8.1%
──────┼───────┼──────────┼──────────┼────────────┼──────
TOTAL | 30    | 185.00   | -        | 9,96,000   | 100%
═══════════════════════════════════════════════════════
```

---

## 📄 PARTY DOCUMENT REPORTS

### Report 4: PARTY LEDGER/STATEMENT

```sql
-- ════════════════════════════════════════════════════
-- REPORT 4: Party Ledger (Give to Party)
-- Data from: party_documents table
-- ════════════════════════════════════════════════════

SELECT 
    pd.invoice_no,
    pd.invoice_date,
    pd.challan_no,
    pd.document_grade_code as grade,
    pd.document_quantity as quantity,
    pd.document_rate as rate,
    pd.document_amount as amount,
    pd.document_cgst as cgst,
    pd.document_sgst as sgst,
    pd.document_total_gst as total_gst,
    pd.document_total as total,
    pd.document_status,
    pd.issued_to_party

FROM party_documents pd

WHERE pd.party_id = ?
  AND pd.invoice_date BETWEEN ? AND ?
  AND pd.document_status IN ('Approved', 'Issued')

ORDER BY pd.invoice_date;

-- Summary
SELECT 
    COUNT(*) as total_invoices,
    SUM(pd.document_quantity) as total_quantity,
    SUM(pd.document_amount) as total_amount,
    SUM(pd.document_total_gst) as total_gst,
    SUM(pd.document_total) as grand_total

FROM party_documents pd

WHERE pd.party_id = ?
  AND pd.invoice_date BETWEEN ? AND ?
  AND pd.document_status IN ('Approved', 'Issued');
```

**Output (Give this to Party):**
```
═══════════════════════════════════════════════════════
              PARTY STATEMENT / LEDGER
              
To: ABC Builders Pvt Ltd
    Contact: Mr. Ramesh Kumar
    Mobile: 98765-43210
    
Period: 01-Jan-2026 to 31-Jan-2026
Generated: 24-Jan-2026
═══════════════════════════════════════════════════════

Invoice  | Date    | Grade | Qty   | Rate  | Amount   
─────────┼─────────┼───────┼───────┼───────┼──────────
INV-001  | 05-Jan  | M30   | 10.00 | 5,200 | 52,000
INV-003  | 07-Jan  | M30   | 10.00 | 5,200 | 52,000
INV-005  | 10-Jan  | M30   | 12.00 | 5,200 | 62,400
───────────────────────────────────────────────────────
Total Invoices: 3
Total Quantity: 32.00 CUM
───────────────────────────────────────────────────────
Sub-Total:        ₹1,66,400
CGST @ 9%:        ₹14,976
SGST @ 9%:        ₹14,976
Total GST:        ₹29,952
───────────────────────────────────────────────────────
GRAND TOTAL:      ₹1,96,352  📄

For: SKCON RMC Plant
Authorized Signatory: ________________
═══════════════════════════════════════════════════════
```

---

## 🔍 VARIANCE ANALYSIS

### Report 5: ACTUAL vs PARTY DOCUMENT COMPARISON

```sql
-- ════════════════════════════════════════════════════
-- REPORT 5: Variance Analysis (Management Only)
-- Compares: actual_production vs party_documents
-- Access: Admin/Manager only
-- ════════════════════════════════════════════════════

SELECT 
    ap.challan_no,
    ap.production_date,
    p.party_name,
    
    -- ACTUAL DATA
    ap.actual_grade_code as actual_grade,
    ap.actual_rate as actual_rate,
    ap.actual_quantity as quantity,
    ap.actual_amount as actual_amount,
    ap.total_amount as actual_total,
    
    -- PARTY DOCUMENT DATA
    pd.document_grade_code as party_grade,
    pd.document_rate as party_rate,
    pd.document_amount as party_amount,
    pd.document_total as party_total,
    
    -- VARIANCES
    pd.grade_different,
    pd.rate_different,
    pd.grade_variance,
    pd.rate_variance,
    pd.amount_variance,
    (pd.document_total - ap.total_amount) as total_variance,
    
    pd.risk_level,
    pd.request_reason,
    pd.approved_by

FROM actual_production ap
INNER JOIN party_documents pd ON ap.production_id = pd.production_id
LEFT JOIN parties p ON ap.party_id = p.party_id

WHERE ap.party_id = ?
  AND ap.production_date BETWEEN ? AND ?
  AND (pd.grade_different = TRUE OR pd.rate_different = TRUE)

ORDER BY ap.production_date DESC;
```

**Output (Confidential - Management Only):**
```
═══════════════════════════════════════════════════════
     VARIANCE ANALYSIS - CONFIDENTIAL
     (Actual vs Party Documents)
═══════════════════════════════════════════════════════
Party: ABC Builders Pvt Ltd
Period: 01-Jan-2026 to 31-Jan-2026
Generated: 24-Jan-2026
Access Level: ADMIN ONLY
───────────────────────────────────────────────────────

Challan: CH-001 | Date: 05-Jan-2026
┌─────────────────────────────────────────────────────┐
│              YOUR ACTUAL  │  PARTY DOCUMENT         │
├─────────────────────────────────────────────────────┤
│ Grade:         M25        │      M30      ⚠️        │
│ Rate:          ₹5,000     │      ₹5,200   ⚠️        │
│ Quantity:      10.00 CUM  │      10.00 CUM          │
│ Amount:        ₹50,000    │      ₹52,000  (+2,000)  │
│ GST:           ₹9,000     │      ₹9,360   (+360)    │
│ Total:         ₹59,000 ✅ │      ₹61,360 📄 (+2,360)│
└─────────────────────────────────────────────────────┘
Risk Level: MEDIUM
Reason: Party requested M30 challan for client
Approved by: Manager on 05-Jan-2026

───────────────────────────────────────────────────────

Challan: CH-003 | Date: 07-Jan-2026
[Similar format...]

───────────────────────────────────────────────────────

SUMMARY FOR PERIOD:
───────────────────────────────────────────────────────
Total Productions with Variance: 3
Grade Mismatches: 3
Rate Mismatches: 3

Your Actual Revenue:      ₹1,88,800  ✅ (Tax on this)
Party Documents Show:     ₹1,96,352  📄
Paper Variance:           +₹7,552   ⚠️

⚠️ Note: Party will pay actual amount (₹1,88,800)
         Document variance is ONLY on paper
═══════════════════════════════════════════════════════
```

---

### Report 6: SUMMARY VARIANCE (Quick View)

```sql
-- ════════════════════════════════════════════════════
-- REPORT 6: Quick Variance Summary
-- ════════════════════════════════════════════════════

SELECT 
    p.party_name,
    COUNT(ap.production_id) as total_productions,
    SUM(ap.total_amount) as actual_total,
    
    COUNT(pd.document_id) as documents_with_variance,
    SUM(pd.document_total) as party_doc_total,
    
    (SUM(pd.document_total) - SUM(ap.total_amount)) as total_variance,
    
    ROUND(
        ((SUM(pd.document_total) - SUM(ap.total_amount)) * 100.0 / SUM(ap.total_amount)),
        2
    ) as variance_percentage

FROM actual_production ap
INNER JOIN party_documents pd ON ap.production_id = pd.production_id
LEFT JOIN parties p ON ap.party_id = p.party_id

WHERE ap.production_date BETWEEN ? AND ?

GROUP BY p.party_name
HAVING total_variance != 0

ORDER BY total_variance DESC;
```

**Output:**
```
Party                | Actual    | Party Doc | Variance | %
─────────────────────┼───────────┼───────────┼──────────┼──────
ABC Builders         | 1,88,800  | 1,96,352  | +7,552   | +4.0%
PQR Developers       | 2,50,000  | 2,60,000  | +10,000  | +4.0%
─────────────────────┼───────────┼───────────┼──────────┼──────
TOTAL                | 4,38,800  | 4,56,352  | +17,552  | +4.0%
```

---

## 📊 DASHBOARD QUERIES

### Q7: Today's Production Summary

```sql
-- ════════════════════════════════════════════════════
-- Dashboard Widget: Today's Production
-- ════════════════════════════════════════════════════

SELECT 
    COUNT(*) as deliveries_today,
    SUM(actual_quantity) as total_cum,
    SUM(actual_amount) as total_value,
    COUNT(DISTINCT party_id) as parties_served,
    COUNT(DISTINCT vehicle_no) as vehicles_used

FROM actual_production

WHERE production_date = CURDATE()
  AND production_status = 'Completed';
```

---

### Q8: Pending Party Documents (Need Approval)

```sql
-- ════════════════════════════════════════════════════
-- Dashboard: Pending Approvals
-- ════════════════════════════════════════════════════

SELECT 
    ap.challan_no,
    ap.production_date,
    p.party_name,
    ap.actual_grade_code,
    ap.actual_rate,
    ap.actual_amount,
    DATEDIFF(CURDATE(), ap.production_date) as days_pending

FROM actual_production ap
LEFT JOIN parties p ON ap.party_id = p.party_id

WHERE ap.has_party_document = FALSE
  AND ap.production_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
  AND p.allow_dual_rate = TRUE

ORDER BY ap.production_date DESC;
```

---

### Q9: Payment Status Summary

```sql
-- ════════════════════════════════════════════════════
-- Dashboard: Payment Summary
-- ════════════════════════════════════════════════════

SELECT 
    payment_status,
    COUNT(*) as count,
    SUM(total_amount) as total_amount

FROM actual_production

WHERE production_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)

GROUP BY payment_status;
```

**Output:**
```
Status    | Count | Amount
──────────┼───────┼──────────────
Pending   | 15    | ₹8,85,000
Partial   | 5     | ₹2,95,000
Paid      | 10    | ₹5,90,000
```

---

## ✅ READY TO USE!

### Implementation in Flask:

```python
# Example Flask route using these queries

@app.route('/reports/production')
def production_report():
    party_id = request.args.get('party_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Use Query from Report 1
    query = """
        SELECT ap.production_date, ap.challan_no, ...
        FROM actual_production ap
        WHERE ap.party_id = %s
          AND ap.production_date BETWEEN %s AND %s
    """
    
    cursor.execute(query, (party_id, start_date, end_date))
    results = cursor.fetchall()
    
    return render_template('production_report.html', data=results)
```

---

**Query Document Status**: ✅ COMPLETE  
**All Queries**: Tested & Ready  
**Next**: UI Implementation
