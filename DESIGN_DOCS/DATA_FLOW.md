# 🔄 DATA FLOW & WORKFLOW DESIGN

**Date**: 24-Jan-2026  
**System**: RMC Production with Dual-Rate Party Documents

---

## 📋 CONTENTS

1. [Overview](#overview)
2. [Workflow Scenarios](#workflow-scenarios)
3. [Data Flow Diagrams](#data-flow-diagrams)
4. [User Journeys](#user-journeys)
5. [Report Generation Flow](#report-generation-flow)

---

## 🎯 OVERVIEW

### Core Concept
```
Production Entry (STEP 1)
        ↓
Actual Data Saved (YOUR BOOKS)
        ↓
    [Decision Point]
        ↓
Party needs different document? 
    ↙         ↘
   YES        NO
    ↓          ↓
Create Party   Use Actual
Document      for Billing
    ↓          ↓
Two Docs      One Doc
```

---

## 🔀 WORKFLOW SCENARIOS

### **Scenario 1: NORMAL PRODUCTION (No Party Document)**

```
┌─────────────────────────────────────────────────────┐
│  SCENARIO 1: Normal Production Flow                 │
│  (Party ko same data chahiye jo actual hai)         │
└─────────────────────────────────────────────────────┘

Step 1: Production Entry
────────────────────────
Operator enters:
  • Date: 05-Jan-2026
  • Party: XYZ Construction
  • Grade: M25
  • Quantity: 10 CUM
  • Rate: ₹5,000
  
[SAVE] button pressed
  ↓
  
Step 2: Data Saved in actual_production
────────────────────────
Database insert:
  ✅ production_id = 1
  ✅ challan_no = CH-001
  ✅ actual_grade = M25
  ✅ actual_rate = 5000
  ✅ actual_amount = 50000
  ✅ has_party_document = FALSE
  
Step 3: Print Challan
────────────────────────
System generates:
  📄 Delivery Challan
     Grade: M25
     Rate: ₹5,000
     Amount: ₹50,000
     
  📄 Tax Invoice (if needed)
     Same as challan
     
✅ DONE! No party document needed.

Data stored in: actual_production table ONLY
```

---

### **Scenario 2: DUAL RATE (Different Rate, Same Grade)**

```
┌─────────────────────────────────────────────────────┐
│  SCENARIO 2: Dual Rate Flow                         │
│  (Party ko same grade, higher rate chahiye)         │
└─────────────────────────────────────────────────────┘

Step 1: Production Entry (Same as Scenario 1)
────────────────────────
Operator enters:
  • Date: 05-Jan-2026
  • Party: ABC Builders
  • Grade: M25
  • Quantity: 10 CUM
  • Rate: ₹5,000 (Your actual rate)
  
[SAVE] pressed
  ↓
  
Step 2: Data Saved in actual_production
────────────────────────
  ✅ production_id = 2
  ✅ actual_grade = M25
  ✅ actual_rate = 5000
  ✅ actual_amount = 50000
  
Step 3: Party Request Popup Appears
────────────────────────
System asks:
  ┌────────────────────────────────────┐
  │ Create Party Document?             │
  ├────────────────────────────────────┤
  │ Party: ABC Builders                │
  │                                    │
  │ Production saved as:               │
  │   Grade: M25 @ ₹5,000              │
  │                                    │
  │ Does party need different billing? │
  │                                    │
  │ [YES - Create Document]  [NO]      │
  └────────────────────────────────────┘
  
Operator clicks: [YES]
  ↓
  
Step 4: Party Document Entry Screen
────────────────────────
Shows:
  Actual Data (Read-only):
    Grade: M25
    Rate: ₹5,000
    Amount: ₹50,000
    
  Party Document Data (Editable):
    Grade: [M25 ▼] (Same)
    Rate: [5200] ← Changed!
    Amount: ₹52,000 (Auto-calculated)
    
  Reason: [Party requested higher rate for billing___]
  Approved by: [Manager ▼]
  
[SAVE PARTY DOCUMENT] pressed
  ↓
  
Step 5: Approval Check
────────────────────────
System checks:
  • Is rate different? YES (5000 → 5200)
  • Does party allow dual rate? Check parties table
  • Is approval required? YES
  • Is approver logged in? Check user role
  
✅ All checks passed
  ↓
  
Step 6: Party Document Saved
────────────────────────
Database insert into party_documents:
  ✅ document_id = 1
  ✅ production_id = 2 (Links to actual)
  ✅ document_grade = M25 (Same)
  ✅ document_rate = 5200 (Different!)
  ✅ document_amount = 52000
  ✅ rate_different = TRUE
  ✅ rate_variance = +200
  
Update actual_production:
  ✅ has_party_document = TRUE
  
Step 7: Print Documents
────────────────────────
System can generate:

  📄 Internal Challan (Your copy)
     From: actual_production
     Grade: M25, Rate: ₹5,000
     
  📄 Party Invoice (Party copy)
     From: party_documents
     Grade: M25, Rate: ₹5,200
     
✅ DONE! Two separate documents.

Data stored in: 
  • actual_production (M25 @ ₹5,000)
  • party_documents (M25 @ ₹5,200)
```

---

### **Scenario 3: GRADE CHANGE (Different Grade)**

```
┌─────────────────────────────────────────────────────┐
│  SCENARIO 3: Grade Change Flow                      │
│  (Party ko different grade chahiye challan pe)      │
└─────────────────────────────────────────────────────┘

Step 1-3: Same as Scenario 2
────────────────────────

Step 4: Party Document Entry
────────────────────────
  Actual Data:
    Grade: M25
    Rate: ₹5,000
    
  Party Document Data:
    Grade: [M30 ▼] ← Changed!
    Rate: [5000] or [6000]
    Amount: ₹50,000 or ₹60,000
    
  ⚠️ WARNING: Grade Mismatch!
    • Actual: M25
    • Document: M30
    • RISK LEVEL: HIGH
    
  Reason: [Party needs M30 challan for client___]
  Written Agreement: [✓] Yes, received
  Approved by: [Senior Manager ▼]
  
[SAVE] pressed
  ↓
  
Step 5: Extra Validation
────────────────────────
System checks:
  • Grade different? YES (M25 → M30)
  • Party allows grade change? Check parties.allow_grade_change
  • Written agreement uploaded? Check
  • Senior approval? Check user role
  
⚠️ If any check fails → REJECT
✅ All passed → Proceed
  ↓
  
Step 6: Party Document Saved
────────────────────────
Database insert:
  ✅ document_grade = M30
  ✅ grade_different = TRUE
  ✅ grade_variance = "M25 → M30"
  ✅ risk_level = HIGH
  ✅ written_agreement = TRUE
  
✅ DONE! High-risk document created.
```

---

### **Scenario 4: COMPLETE MISMATCH (Grade + Rate Both Different)**

```
┌─────────────────────────────────────────────────────┐
│  SCENARIO 4: Complete Mismatch                      │
│  (Dono different - Grade bhi, Rate bhi)             │
└─────────────────────────────────────────────────────┘

Actual Production:
  Grade: M25
  Rate: ₹5,000
  Amount: ₹50,000
  
Party Document:
  Grade: M30 (Different)
  Rate: ₹5,200 (Different)
  Amount: ₹52,000
  
Variances:
  • grade_different = TRUE
  • rate_different = TRUE
  • grade_variance = "M25 → M30"
  • rate_variance = +200
  • amount_variance = +2000
  • risk_level = HIGH

Extra Requirements:
  • Manager approval mandatory
  • Written agreement mandatory
  • Audit log entry created
  • Email notification to admin
```

---

## 📊 DATA FLOW DIAGRAMS

### **Flow 1: Production to Database**

```
┌──────────────┐
│  User Input  │
│  (Web Form)  │
└──────┬───────┘
       │
       ↓
┌──────────────────────────┐
│  Flask Route Handler     │
│  @app.route('/production│
│          /create')       │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  Validate Input          │
│  • Party exists?         │
│  • Grade valid?          │
│  • Quantity > 0?         │
└──────────┬───────────────┘
           │
           ↓ ✅ Valid
┌──────────────────────────┐
│  Calculate Amounts       │
│  • Amount = Qty × Rate   │
│  • GST = Amount × 18%    │
│  • Total = Amount + GST  │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  INSERT into             │
│  actual_production       │
│                          │
│  ✅ Data saved           │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  Return Success          │
│  • production_id         │
│  • challan_no            │
└──────────────────────────┘
```

---

### **Flow 2: Party Document Creation**

```
┌──────────────────────┐
│  User Clicks:        │
│  "Create Party Doc"  │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────────┐
│  Load Production Data    │
│  FROM actual_production  │
│  WHERE production_id = ? │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  Show Form with:         │
│  • Actual data (readonly)│
│  • Editable doc fields   │
└──────────┬───────────────┘
           │
           ↓ User fills & submits
┌──────────────────────────┐
│  Validation Checks       │
│  1. Party allows dual?   │
│  2. Approval needed?     │
│  3. User has permission? │
│  4. Risk acceptable?     │
└──────────┬───────────────┘
           │
           ↓ ✅ All checks OK
┌──────────────────────────┐
│  Calculate Variances     │
│  • grade_different?      │
│  • rate_variance         │
│  • amount_variance       │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  INSERT into             │
│  party_documents         │
│                          │
│  ✅ Document saved       │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  UPDATE actual_production│
│  SET has_party_document  │
│      = TRUE              │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  Return Success          │
│  • document_id           │
│  • invoice_no            │
└──────────────────────────┘
```

---

### **Flow 3: Report Generation**

```
┌──────────────────────┐
│  User Selects:       │
│  • Report Type       │
│  • Party             │
│  • Date Range        │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────────────────────┐
│  Report Type Decision                │
├──────────────────────────────────────┤
│  1. Your Production Report           │
│  2. Party Document Report            │
│  3. Variance Analysis                │
└──────────┬───────────────────────────┘
           │
           ├─────────────────────┬─────────────────┐
           ↓                     ↓                 ↓
    ┌──────────────┐    ┌──────────────┐  ┌──────────────┐
    │  QUERY 1:    │    │  QUERY 2:    │  │  QUERY 3:    │
    │  actual_     │    │  party_      │  │  Both tables │
    │  production  │    │  documents   │  │  + JOIN      │
    └──────┬───────┘    └──────┬───────┘  └──────┬───────┘
           │                   │                  │
           ↓                   ↓                  ↓
    ┌──────────────┐    ┌──────────────┐  ┌──────────────┐
    │  Shows M25   │    │  Shows M30   │  │  Shows both  │
    │  @ ₹5,000    │    │  @ ₹5,200    │  │  side by side│
    └──────┬───────┘    └──────┬───────┘  └──────┬───────┘
           │                   │                  │
           └───────────────────┴──────────────────┘
                              │
                              ↓
                   ┌──────────────────────┐
                   │  Format as:          │
                   │  • HTML (screen)     │
                   │  • PDF (download)    │
                   │  • Excel (export)    │
                   └──────────────────────┘
```

---

## 👤 USER JOURNEYS

### **Journey 1: Operator - Normal Production Entry**

```
TIME: ~2 minutes

1. Login to system
   ↓
2. Click "Production Entry"
   ↓
3. Fill form:
   - Date: Auto-filled (today)
   - Party: Select from dropdown
   - Site: Select from dropdown
   - Grade: Select M25
   - Quantity: Enter 10
   - Rate: Auto-filled (₹5,000)
   - Vehicle: Enter MH12AB1234
   - Driver: Enter Ram Kumar
   ↓
4. Click [Save Production]
   ↓
5. Success message:
   "Production saved! Challan: CH-001"
   ↓
6. Click [Print Challan]
   ↓
7. Challan printed
   ↓
8. ✅ DONE!

Tables affected:
  • actual_production: 1 INSERT
```

---

### **Journey 2: Manager - Dual Rate Approval**

```
TIME: ~5 minutes

1. Operator creates production (Journey 1)
   ↓
2. Operator says: "Party wants ₹5,200 rate"
   ↓
3. Manager login to system
   ↓
4. Goes to "Pending Approvals" OR
   Production entry → "Create Party Doc"
   ↓
5. Sees actual production:
   CH-001, M25, ₹5,000
   ↓
6. Clicks [Create Party Document]
   ↓
7. Fills party document form:
   - Grade: M25 (same)
   - Rate: ₹5,200 (changed)
   - Reason: "Party request"
   - Agreement: Upload file
   ↓
8. System shows warning:
   ⚠️ Rate variance: +₹200/CUM
   ⚠️ Total variance: +₹2,000
   ↓
9. Manager reviews and clicks [Approve & Save]
   ↓
10. Success:
    "Party document created: INV-001"
    ↓
11. Click [Print Party Invoice]
    ↓
12. Invoice printed (shows ₹5,200)
    ↓
13. ✅ DONE!

Tables affected:
  • party_documents: 1 INSERT
  • actual_production: 1 UPDATE (has_party_document)
```

---

### **Journey 3: Accountant - Generate Reports**

```
TIME: ~1 minute

FOR YOUR BOOKS:
───────────────
1. Login to system
   ↓
2. Click "Reports" → "Production Reports"
   ↓
3. Select:
   - Report: "Your Production Report"
   - Party: ABC Builders
   - Date: 01-Jan to 31-Jan
   ↓
4. Click [Generate]
   ↓
5. Report shows:
   Data from: actual_production table ONLY
   Grade: M25
   Rate: ₹5,000
   Total: ₹50,000
   ↓
6. Click [Export PDF]
   ↓
7. File saved: production_report_jan2026.pdf
   ↓
8. ✅ File GST return with this!

FOR PARTY:
──────────
1. Same steps 1-3
   ↓
2. Select:
   - Report: "Party Document Report"
   ↓
3. Report shows:
   Data from: party_documents table ONLY
   Grade: M30
   Rate: ₹5,200
   Total: ₹52,000
   ↓
4. Click [Email to Party]
   ↓
5. ✅ Party receives their report!
```

---

## 🔄 COMPLETE SYSTEM FLOW (End-to-End)

```
DAY 1: PRODUCTION
═════════════════

08:00 AM - Plant Operator
├─ Creates production entry
├─ Grade: M25, Qty: 10 CUM
├─ Rate: ₹5,000
└─ Saves → actual_production table

09:00 AM - Manager receives call from party
├─ Party: "Hume M30 ka challan chahiye"
└─ Manager: "Ok, I'll create document"

09:15 AM - Manager
├─ Opens system
├─ Finds production CH-001
├─ Creates party document
├─ Grade: M30, Rate: ₹5,200
├─ Uploads party's written request
├─ Approves and saves
└─ Prints invoice for party → party_documents table

10:00 AM - Documents sent
├─ Internal challan (M25, ₹5,000) → to accounts dept
└─ Party invoice (M30, ₹5,200) → to party via email


DAY 31: MONTH END
══════════════════

Accountant - YOUR BOOKS
├─ Generates report from actual_production
├─ Total: ₹1,50,000 (30 CUM × ₹5,000)
└─ Files GST return with this amount

Accountant - PARTY STATEMENT
├─ Generates report from party_documents
├─ Total: ₹1,56,000 (30 CUM × ₹5,200)
└─ Sends to party for reconciliation

Management - VARIANCE CHECK
├─ Generates variance report
├─ Actual revenue: ₹1,50,000
├─ Party documents show: ₹1,56,000
├─ Paper variance: +₹6,000
└─ Actual payment received: ₹1,50,000 ✅


AUDIT TIME
══════════

Auditor asks: "Show production records"
├─ Show: actual_production table
├─ Data: M25 @ ₹5,000
└─ ✅ Clean, no issues

Party asks: "Our records show ₹1,56,000"
├─ Show: party_documents table
├─ Data: M30 @ ₹5,200
└─ ✅ Matches their requirement

All data reconciled, no confusion! 🎯
```

---

## ✅ KEY TAKEAWAYS

### 1. **Two Independent Flows**
```
Actual Production Flow (Mandatory)
  → Always created
  → Your truth
  → Tax filing basis

Party Document Flow (Optional)
  → Created only when needed
  → Party's requirement
  → Separate from actual
```

### 2. **No Data Mixing**
```
❌ WRONG: Store both in one record
✅ RIGHT: Two separate tables linked by ID
```

### 3. **Clear Reporting**
```
Your Report   → Query actual_production
Party Report  → Query party_documents
Variance      → JOIN both tables
```

### 4. **Access Control**
```
Operator    → Can create production only
Manager     → Can create party documents
Accountant  → Can view all reports
Admin       → Can see variance analysis
```

---

**Flow Design Status**: ✅ COMPLETE  
**Next**: UI Wireframes & SQL Queries
