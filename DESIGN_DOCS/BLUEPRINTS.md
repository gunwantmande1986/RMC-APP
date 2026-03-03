# 📐 TECHNICAL BLUEPRINTS - RMC Production System

**Design Document**: UI/UX Wireframes - AutoCAD Style  
**Date**: 24-Jan-2026  
**Version**: 1.0

---

## 📋 TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Screen Blueprints](#screen-blueprints)
3. [Database ER Diagram](#database-er-diagram)
4. [Report Layouts](#report-layouts)
5. [User Flow Diagrams](#user-flow-diagrams)

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RMC PLANT ERP - SYSTEM ARCHITECTURE             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │   Browser    │  │   Mobile     │  │   Tablet     │  │   Print    ││
│  │   (Chrome)   │  │   (App)      │  │   (iPad)     │  │  (PDF)     ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘│
│         │                  │                  │                │       │
└─────────┼──────────────────┼──────────────────┼────────────────┼───────┘
          │                  │                  │                │
          └──────────────────┴──────────────────┴────────────────┘
                                     │
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER (Flask)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  ROUTES & CONTROLLERS                                            │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │  /production/entry          /production/save                     │ │
│  │  /party-document/create     /party-document/save                 │ │
│  │  /reports/production        /reports/party-statement             │ │
│  │  /reports/variance          /api/dashboard                       │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  BUSINESS LOGIC                                                  │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │  • Production Entry Logic     • Validation Rules                 │ │
│  │  • Party Document Creation    • Approval Workflow                │ │
│  │  • Report Generation          • Access Control                   │ │
│  │  • Variance Calculation       • GST Calculation                  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER (MySQL)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │   PARTIES    │  │    SITES     │  │   GRADES     │  │   USERS    ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘│
│                                                                         │
│  ┌───────────────────────────────┐  ┌───────────────────────────────┐│
│  │   ACTUAL_PRODUCTION ⭐        │  │   PARTY_DOCUMENTS ⭐          ││
│  │   (Your Truth - M25/₹5000)    │  │   (Their Request - M30/₹5200) ││
│  └───────────────────────────────┘  └───────────────────────────────┘│
│                                                                         │
│  ┌──────────────┐                                                      │
│  │ PUMP_SERVICES│                                                      │
│  └──────────────┘                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ DATABASE ER DIAGRAM (AutoCAD Style)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    DATABASE ENTITY-RELATIONSHIP DIAGRAM                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

                    ┌─────────────────────────┐
                    │       PARTIES           │
                    │─────────────────────────│
                    │ PK party_id             │
                    │    party_code           │
                    │    party_name           │
                    │    mobile               │
                    │    gst_no               │
                    │    allow_dual_rate      │◄────┐
                    │    allow_grade_change   │     │
                    └─────────────────────────┘     │
                             │                      │
                             │ 1                    │
                             │                      │
                             │ has many             │
                             ↓ N                    │
                    ┌─────────────────────────┐     │
                    │        SITES            │     │
                    │─────────────────────────│     │
                    │ PK site_id              │     │
                    │ FK party_id             │─────┘
                    │    site_name            │
                    │    address              │
                    │    distance_km          │
                    └─────────────────────────┘
                             │
                             │ 1
                             │
                             │ has many
                             ↓ N
     ┌──────────────────────────────────────────────────────────────────┐
     │                   ACTUAL_PRODUCTION ⭐                            │
     │                   (YOUR TRUTH - Never Mixed)                     │
     │──────────────────────────────────────────────────────────────────│
     │ PK  production_id                                                │
     │ FK  party_id              ────┐                                  │
     │ FK  site_id               ────┼──┐                               │
     │ FK  actual_grade_id       ────┼──┼───┐                           │
     │     challan_no (UNIQUE)       │  │   │                           │
     │     production_date           │  │   │                           │
     │                               │  │   │                           │
     │ 📊 ACTUAL DATA (PURE):        │  │   │                           │
     │     actual_grade_code         │  │   │                           │
     │     actual_quantity           │  │   │                           │
     │     actual_rate               │  │   │                           │
     │     actual_amount             │  │   │                           │
     │     total_gst                 │  │   │                           │
     │     total_amount              │  │   │                           │
     │                               │  │   │                           │
     │     vehicle_no                │  │   │                           │
     │     driver_name               │  │   │                           │
     │     mix_design_code           │  │   │                           │
     │     delivery_status           │  │   │                           │
     │     payment_status            │  │   │                           │
     │                               │  │   │                           │
     │     has_party_document ──────┐│  │   │                           │
     └──────────────────────────────┼┘  │   │                           │
                    │               │   │   │                           │
                    │ 1             │   │   │                           │
                    │               │   │   │                           │
                    │ has zero      │   │   │                           │
                    │ or one        │   │   │                           │
                    ↓ 0..1          │   │   │                           │
     ┌──────────────────────────────┼───┼───┼───────────────────────────┐
     │            PARTY_DOCUMENTS ⭐ │   │   │                           │
     │            (THEIR REQUEST - Separate)                            │
     │──────────────────────────────────────────────────────────────────│
     │ PK  document_id                                                  │
     │ FK  production_id         ───┘                                   │
     │ FK  party_id              ────────┘                              │
     │ FK  document_grade_id     ────────────┘                          │
     │     challan_no (Same)                                            │
     │     invoice_no (UNIQUE)                                          │
     │     invoice_date                                                 │
     │                                                                  │
     │ 📄 PARTY DOCUMENT DATA (SEPARATE):                               │
     │     document_grade_code                                          │
     │     document_quantity                                            │
     │     document_rate                                                │
     │     document_amount                                              │
     │     document_total_gst                                           │
     │     document_total                                               │
     │                                                                  │
     │ ⚠️  VARIANCE TRACKING:                                           │
     │     grade_different (BOOL)                                       │
     │     rate_different (BOOL)                                        │
     │     grade_variance                                               │
     │     rate_variance                                                │
     │     amount_variance                                              │
     │                                                                  │
     │ 🔐 AUTHORIZATION:                                                │
     │     request_reason                                               │
     │     requested_by                                                 │
     │     approved_by                                                  │
     │     approval_date                                                │
     │     written_agreement (BOOL)                                     │
     │     risk_level                                                   │
     │     document_status                                              │
     └──────────────────────────────────────────────────────────────────┘


                    ┌─────────────────────────┐
                    │       GRADES            │
                    │─────────────────────────│
                    │ PK grade_id             │
                    │    grade_code (M20,M25) │
                    │    grade_name           │
                    │    cement_content       │
                    │    base_rate            │
                    │    mix_design_code      │
                    └─────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                      PUMP_SERVICES                               │
     │──────────────────────────────────────────────────────────────────│
     │ PK  service_id                                                   │
     │ FK  party_id                                                     │
     │ FK  site_id                                                      │
     │     service_no                                                   │
     │     service_date                                                 │
     │     pump_type (28M, 32M, 36M)                                    │
     │     start_time / end_time                                        │
     │     total_hours                                                  │
     │     rate_per_hour                                                │
     │     amount                                                       │
     │     gst_amount                                                   │
     │     total_amount                                                 │
     └──────────────────────────────────────────────────────────────────┘


                    ┌─────────────────────────┐
                    │        USERS            │
                    │─────────────────────────│
                    │ PK user_id              │
                    │    username             │
                    │    password_hash        │
                    │    full_name            │
                    │    role                 │
                    │    can_create_production│
                    │    can_create_party_doc │
                    │    can_approve_dual_rate│
                    │    can_view_variance    │
                    └─────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════╗
║  KEY RELATIONSHIPS:                                                       ║
║  ─────────────                                                            ║
║  • PARTIES (1) ───> (N) SITES                                            ║
║  • PARTIES (1) ───> (N) ACTUAL_PRODUCTION                                ║
║  • ACTUAL_PRODUCTION (1) ───> (0..1) PARTY_DOCUMENTS                     ║
║  • GRADES (1) ───> (N) ACTUAL_PRODUCTION                                 ║
║  • GRADES (1) ───> (N) PARTY_DOCUMENTS                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 🖥️ SCREEN BLUEPRINT 1: PRODUCTION ENTRY

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ☰ RMC PLANT ERP                    Plant A - XYZ     👤 Gunvant  🔔  ⚙️  ⎋│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─┐                                                                        │
│  │▼│ MAIN MENU                  📊 PRODUCTION ENTRY FORM                    │
│  └─┘                            ═══════════════════════                    │
│   📊 Dashboard                                                              │
│   💰 Cash Production   ◄─── YOU ARE HERE                                   │
│   📄 Billing Production                                                     │
│   📋 Generate Invoice          ┌────────────────────────────────────────┐  │
│   📦 Purchase Entry            │  📋 BASIC INFORMATION                  │  │
│   💳 Payment Entry             ├────────────────────────────────────────┤  │
│   ⛽ Diesel Management          │                                        │  │
│   🚚 Delivery Challans          │  Date: [05-Jan-2026      ▼] 📅        │  │
│                                │  Time: [10:30 AM         ▼] ⏰        │  │
│  PUMP SERVICES                 │                                        │  │
│   💧 Cash Pump Service          │  Challan No: [CH-001] (Auto)          │  │
│   📄 Billing Pump Service       │                                        │  │
│   📊 Pump Master                │  Party: [ABC Builders Pvt Ltd    ▼]   │  │
│                                │                                        │  │
│  REPORTS                       │  Site: [Construction Site - Pune ▼]   │  │
│   📈 Production Reports         │                                        │  │
│   📊 Sales Reports              │  Distance: 15.5 km                    │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
│                                ┌────────────────────────────────────────┐  │
│                                │  🏗️ PRODUCTION DETAILS                │  │
│                                ├────────────────────────────────────────┤  │
│                                │                                        │  │
│                                │  Grade: [M25 ▼]                        │  │
│                                │                                        │  │
│                                │  Mix Design: [M25-Mix-001 ▼]           │  │
│                                │                                        │  │
│                                │  Quantity: [10.00] CUM                 │  │
│                                │                                        │  │
│                                │  Rate: ₹ [5,000.00] /CUM               │  │
│                                │         (Default from grade master)    │  │
│                                │                                        │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
│                                ┌────────────────────────────────────────┐  │
│                                │  🚚 DELIVERY DETAILS                   │  │
│                                ├────────────────────────────────────────┤  │
│                                │                                        │  │
│                                │  Vehicle No: [MH12AB1234]              │  │
│                                │                                        │  │
│                                │  Driver: [Ram Kumar           ▼]       │  │
│                                │                                        │  │
│                                │  Mobile: [98765-43210]                 │  │
│                                │                                        │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
│                                ┌────────────────────────────────────────┐  │
│                                │  💰 AMOUNT CALCULATION                 │  │
│                                ├────────────────────────────────────────┤  │
│                                │                                        │  │
│                                │  Amount:          ₹50,000.00           │  │
│                                │  CGST @ 9%:       ₹4,500.00            │  │
│                                │  SGST @ 9%:       ₹4,500.00            │  │
│                                │  ─────────────────────────             │  │
│                                │  Total GST:       ₹9,000.00            │  │
│                                │  ═════════════════════════             │  │
│                                │  GRAND TOTAL:     ₹59,000.00 ✅        │  │
│                                │                                        │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
│                                ┌────────────────────────────────────────┐  │
│                                │  📝 NOTES                              │  │
│                                ├────────────────────────────────────────┤  │
│                                │  [Normal delivery, no issues______]    │  │
│                                │                                        │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
│                                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐  │
│  │ 💾 SAVE PRODUCTION   │  │ 🖨️ PRINT CHALLAN    │  │ ❌ CANCEL      │  │
│  └──────────────────────┘  └──────────────────────┘  └────────────────┘  │
│                                                                             │
│                                After saving:                                │
│                                ┌────────────────────────────────────────┐  │
│                                │ ✅ Success!                            │  │
│                                │ Production saved: CH-001               │  │
│                                │                                        │  │
│                                │ Party needs different document?        │  │
│                                │                                        │  │
│                                │ [YES - Create Party Doc] [NO - Done]  │  │
│                                └────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

╔═════════════════════════════════════════════════════════════════════════════╗
║  DIMENSIONS: 1920px × 1080px (Full HD)                                     ║
║  GRID: 12-column responsive layout                                         ║
║  SIDEBAR: 250px fixed                                                      ║
║  MAIN CONTENT: calc(100% - 250px)                                          ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 🖥️ SCREEN BLUEPRINT 2: PARTY DOCUMENT CREATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ☰ RMC PLANT ERP                    Plant A - XYZ     👤 Manager  🔔  ⚙️  ⎋│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📄 CREATE PARTY DOCUMENT (Separate from Actual Production)                │
│  ═══════════════════════════════════════════════════════════════           │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  🔗 LINKED TO PRODUCTION                                           │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │  Challan No: CH-001                                                │   │
│  │  Production Date: 05-Jan-2026                                      │   │
│  │  Party: ABC Builders Pvt Ltd                                       │   │
│  │  Site: Construction Site - Pune                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐ │
│  │  ✅ ACTUAL PRODUCTION (Locked)  │  │  📄 PARTY DOCUMENT (Editable)   │ │
│  │  ════════════════════════════   │  │  ═══════════════════════════    │ │
│  │  (Read-only - Your Truth)       │  │  (What party wants on paper)    │ │
│  ├─────────────────────────────────┤  ├─────────────────────────────────┤ │
│  │                                 │  │                                 │ │
│  │  Grade: M25 🔒                  │  │  Grade: [M30 ▼] ⚠️ Different   │ │
│  │                                 │  │                                 │ │
│  │  Quantity: 10.00 CUM 🔒         │  │  Quantity: [10.00] CUM          │ │
│  │                                 │  │                                 │ │
│  │  Rate: ₹5,000 /CUM 🔒           │  │  Rate: ₹ [5,200.00] /CUM ⚠️     │ │
│  │                                 │  │                                 │ │
│  │  Amount: ₹50,000 🔒             │  │  Amount: ₹52,000 (Auto calc)    │ │
│  │                                 │  │                                 │ │
│  │  CGST: ₹4,500 🔒                │  │  CGST: ₹4,680                   │ │
│  │  SGST: ₹4,500 🔒                │  │  SGST: ₹4,680                   │ │
│  │  ──────────────                 │  │  ──────────────                 │ │
│  │  GST: ₹9,000 🔒                 │  │  GST: ₹9,360                    │ │
│  │  ══════════════                 │  │  ══════════════                 │ │
│  │  TOTAL: ₹59,000 ✅              │  │  TOTAL: ₹61,360 📄              │ │
│  │                                 │  │                                 │ │
│  └─────────────────────────────────┘  └─────────────────────────────────┘ │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  ⚠️ VARIANCE DETECTED!                                             │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │                                                                    │   │
│  │  Grade Mismatch:   M25 → M30  (Upgrade shown) 🔴                  │   │
│  │  Rate Variance:    +₹200/CUM                                      │   │
│  │  Amount Variance:  +₹2,000                                        │   │
│  │  GST Variance:     +₹360                                          │   │
│  │  Total Variance:   +₹2,360 (on paper only)                        │   │
│  │                                                                    │   │
│  │  Risk Level:       🔴 HIGH                                         │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  🔐 AUTHORIZATION REQUIRED                                         │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │                                                                    │   │
│  │  Invoice No: [INV-001] (Auto-generated)                           │   │
│  │                                                                    │   │
│  │  Invoice Date: [05-Jan-2026 ▼]                                    │   │
│  │                                                                    │   │
│  │  Document Type: [Tax Invoice ▼]                                   │   │
│  │                                                                    │   │
│  │  Reason for Variance:                                             │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │ Party requested M30 grade challan for their client          │ │   │
│  │  │ presentation. Written agreement received from party.        │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  │  Requested by (Party): [Ramesh Kumar (ABC Builders)]              │   │
│  │                                                                    │   │
│  │  Approved by: [Manager ▼]  Date: [05-Jan-2026]                   │   │
│  │                                                                    │   │
│  │  ☑ Written agreement received from party                          │   │
│  │  ☑ Party accepts liability for grade variance                     │   │
│  │  ☐ Upload agreement scan: [Choose File...]                        │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│                                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐  │
│  │ ✅ APPROVE & SAVE    │  │ 🖨️ PRINT INVOICE    │  │ ❌ CANCEL      │  │
│  └──────────────────────┘  └──────────────────────┘  └────────────────┘  │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

╔═════════════════════════════════════════════════════════════════════════════╗
║  ACCESS CONTROL: Manager/Admin only                                        ║
║  APPROVAL: Mandatory for grade/rate variance                               ║
║  RISK LEVEL: Calculated automatically                                      ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 🖥️ SCREEN BLUEPRINT 3: REPORT GENERATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ☰ RMC PLANT ERP                    Plant A - XYZ     👤 Accountant 🔔 ⚙️ ⎋│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 PRODUCTION & PARTY REPORTS                                              │
│  ═══════════════════════════════                                           │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  🔍 FILTERS & SELECTION                                            │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │                                                                    │   │
│  │  Party:  [ABC Builders Pvt Ltd          ▼]                        │   │
│  │                                                                    │   │
│  │  Date Range:  [01-Jan-2026 📅] to [31-Jan-2026 📅]                │   │
│  │                                                                    │   │
│  │  Quick Filters:                                                   │   │
│  │  [Today] [This Week] [This Month] [Last Month] [This FY]         │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  📋 SELECT REPORT TYPE                                             │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │                                                                    │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │  ⚫ YOUR PRODUCTION REPORT (Internal - For Accounts)         │ │   │
│  │  ├──────────────────────────────────────────────────────────────┤ │   │
│  │  │  Data Source: actual_production table                        │ │   │
│  │  │  Shows: M25 @ ₹5,000 (Actual supply data)                    │ │   │
│  │  │  Purpose: Tax filing, GST return, Internal accounting        │ │   │
│  │  │  Period Total: ₹1,88,800                                     │ │   │
│  │  │  Access: All users                                           │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │  ⚪ PARTY STATEMENT REPORT (Give to Party)                   │ │   │
│  │  ├──────────────────────────────────────────────────────────────┤ │   │
│  │  │  Data Source: party_documents table                          │ │   │
│  │  │  Shows: M30 @ ₹5,200 (Party requested data)                  │ │   │
│  │  │  Purpose: Party ledger, Customer statement                   │ │   │
│  │  │  Period Total: ₹1,96,352                                     │ │   │
│  │  │  Access: All users                                           │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │  ⚪ VARIANCE ANALYSIS (Management Review) 🔒 Admin Only      │ │   │
│  │  ├──────────────────────────────────────────────────────────────┤ │   │
│  │  │  Data Source: Both tables (JOIN)                             │ │   │
│  │  │  Shows: Side-by-side comparison                              │ │   │
│  │  │  Purpose: Internal review, Audit trail                       │ │   │
│  │  │  Variance: +₹7,552 (on paper)                                │ │   │
│  │  │  Access: Admin/Manager only                                  │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │  ⚪ DATE-WISE SUMMARY                                         │ │   │
│  │  │  ⚪ GRADE-WISE SUMMARY                                        │ │   │
│  │  │  ⚪ SITE-WISE SUMMARY                                         │ │   │
│  │  │  ⚪ DELIVERY CHALLAN REGISTER                                 │ │   │
│  │  │  ⚪ PUMP SERVICE REPORT                                       │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ 🔍 GENERATE │  │ 📥 Export   │  │ 🖨️ Print   │  │ 📧 Email Party │  │
│  │   REPORT    │  │    PDF      │  │   Report    │  │                 │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘  │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  📄 REPORT PREVIEW                                                 │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │  ═══════════════════════════════════════════════════════     │ │   │
│  │  │       YOUR PRODUCTION REPORT (Internal)                      │ │   │
│  │  │  ═══════════════════════════════════════════════════════     │ │   │
│  │  │  Party: ABC Builders Pvt Ltd                                 │ │   │
│  │  │  Period: 01-Jan-2026 to 31-Jan-2026                          │ │   │
│  │  │  Generated: 24-Jan-2026 10:30 AM                             │ │   │
│  │  │  ─────────────────────────────────────────────────────────   │ │   │
│  │  │                                                              │ │   │
│  │  │  Date  │Challan│Grade│Qty  │Rate │Amount │GST   │Total     │ │   │
│  │  │  ──────┼───────┼─────┼─────┼─────┼───────┼──────┼─────────│ │   │
│  │  │  05-Jan│CH-001 │ M25 │10.00│5,000│50,000 │9,000 │ 59,000  │ │   │
│  │  │  07-Jan│CH-003 │ M25 │10.00│5,000│50,000 │9,000 │ 59,000  │ │   │
│  │  │  10-Jan│CH-005 │ M25 │12.00│5,000│60,000 │10,800│ 70,800  │ │   │
│  │  │  ──────┼───────┼─────┼─────┼─────┼───────┼──────┼─────────│ │   │
│  │  │  TOTAL:  3      32.00       1,60,000  28,800  1,88,800 ✅  │ │   │
│  │  │  ═══════════════════════════════════════════════════════     │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  │                                                                    │   │
│  │  [Scroll for more data...]                                        │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

╔═════════════════════════════════════════════════════════════════════════════╗
║  FEATURES:                                                                  ║
║  • Real-time filtering                                                      ║
║  • Export: PDF, Excel, CSV                                                  ║
║  • Email directly to party                                                  ║
║  • Print-friendly view                                                      ║
║  • Date range picker                                                        ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 📄 REPORT LAYOUT: YOUR PRODUCTION REPORT (Print View)

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║                            SKCON RMC PLANT                                  ║
║                     Enterprise Management System                            ║
║                                                                             ║
║              Plant: Plant A - XYZ  |  GSTIN: 27XXXXX1234X1Z5              ║
║              Address: Industrial Area, Pune - 411001                        ║
║              Phone: +91 98765-43210  |  Email: info@skconrmc.com          ║
║                                                                             ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║                     PRODUCTION REPORT (INTERNAL)                            ║
║                     ════════════════════════════════                        ║
║                                                                             ║
║  Party Name:     ABC Builders Pvt Ltd                                      ║
║  Party Code:     P001                                                       ║
║  Contact:        Mr. Ramesh Kumar                                          ║
║  Mobile:         +91 98765-43210                                           ║
║  GST No:         27AAAAA1234A1Z5                                           ║
║                                                                             ║
║  Period:         01-Jan-2026 to 31-Jan-2026                                ║
║  Report Date:    24-Jan-2026 10:30 AM                                      ║
║  Generated By:   Gunvant Admin                                             ║
║  Report Type:    Actual Production (For Tax Filing)                        ║
║                                                                             ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  ┌───┬──────────┬─────────┬───────┬──────┬────────┬──────────┬──────────┐ ║
║  │Sr.│   Date   │ Challan │ Grade │ Qty  │  Rate  │  Amount  │  Total   │ ║
║  │No.│          │   No.   │       │(CUM) │(₹/CUM) │   (₹)    │   (₹)    │ ║
║  ├───┼──────────┼─────────┼───────┼──────┼────────┼──────────┼──────────┤ ║
║  │ 1 │05-Jan-26 │ CH-001  │  M25  │10.00 │ 5,000  │  50,000  │  59,000  │ ║
║  │ 2 │07-Jan-26 │ CH-003  │  M25  │10.00 │ 5,000  │  50,000  │  59,000  │ ║
║  │ 3 │10-Jan-26 │ CH-005  │  M25  │12.00 │ 5,000  │  60,000  │  70,800  │ ║
║  │ 4 │12-Jan-26 │ CH-008  │  M30  │ 8.00 │ 6,000  │  48,000  │  56,640  │ ║
║  │ 5 │15-Jan-26 │ CH-012  │  M25  │10.00 │ 5,000  │  50,000  │  59,000  │ ║
║  │ 6 │18-Jan-26 │ CH-016  │  M35  │ 7.00 │ 7,000  │  49,000  │  57,820  │ ║
║  │ 7 │20-Jan-26 │ CH-020  │  M25  │11.00 │ 5,000  │  55,000  │  64,900  │ ║
║  │ 8 │22-Jan-26 │ CH-024  │  M30  │ 9.00 │ 6,000  │  54,000  │  63,720  │ ║
║  │ 9 │25-Jan-26 │ CH-028  │  M25  │10.00 │ 5,000  │  50,000  │  59,000  │ ║
║  │10 │28-Jan-26 │ CH-032  │  M25  │12.00 │ 5,000  │  60,000  │  70,800  │ ║
║  └───┴──────────┴─────────┴───────┴──────┴────────┴──────────┴──────────┘ ║
║                                                                             ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │                        SUMMARY TOTALS                               │  ║
║  ├─────────────────────────────────────────────────────────────────────┤  ║
║  │  Total Deliveries (Trips):               10                         │  ║
║  │  Total Quantity Supplied:                99.00 CUM                  │  ║
║  │  ─────────────────────────────────────────────────────────────      │  ║
║  │  Sub-Total (Before Tax):                 ₹5,26,000                  │  ║
║  │  CGST @ 9%:                              ₹47,340                    │  ║
║  │  SGST @ 9%:                              ₹47,340                    │  ║
║  │  ─────────────────────────────────────────────────────────────      │  ║
║  │  Total GST @ 18%:                        ₹94,680                    │  ║
║  │  ═════════════════════════════════════════════════════════════      │  ║
║  │  GRAND TOTAL:                            ₹6,20,680  ✅              │  ║
║  │  ═════════════════════════════════════════════════════════════      │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                             ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │                    GRADE-WISE BREAKUP                               │  ║
║  ├─────────────────────────────────────────────────────────────────────┤  ║
║  │  M20 Grade:   0.00 CUM  (0%)      ₹0                                │  ║
║  │  M25 Grade:   75.00 CUM (75.8%)   ₹4,43,250                         │  ║
║  │  M30 Grade:   17.00 CUM (17.2%)   ₹1,00,260                         │  ║
║  │  M35 Grade:   7.00 CUM  (7.1%)    ₹41,090                           │  ║
║  │  M40 Grade:   0.00 CUM  (0%)      ₹0                                │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                             ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │  ⚠️ IMPORTANT NOTE:                                                 │  ║
║  │  • This is your ACTUAL PRODUCTION data                              │  ║
║  │  • Use this report for GST filing and tax returns                   │  ║
║  │  • This represents real supply quantities and rates                 │  ║
║  │  • For party-specific documents, generate Party Statement Report    │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                             ║
║                                                                             ║
║  For SKCON RMC Plant                                                       ║
║  Authorized Signatory: _______________________                             ║
║                                                                             ║
║                                                          Page 1 of 1        ║
╚═════════════════════════════════════════════════════════════════════════════╝

╔═════════════════════════════════════════════════════════════════════════════╗
║  PAPER SIZE: A4 (210mm × 297mm)                                            ║
║  MARGINS: Top: 15mm, Bottom: 15mm, Left: 15mm, Right: 15mm                ║
║  FONT: Monospace for alignment, Sans-serif for text                        ║
║  PRINT: Black & White or Color                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 USER FLOW DIAGRAM: Complete Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE USER FLOW DIAGRAM                              │
└─────────────────────────────────────────────────────────────────────────────┘


START: User Login
      │
      ↓
┌─────────────────┐
│  Authentication │
│  Username/Pass  │
└─────────────────┘
      │
      ↓
┌─────────────────┐
│   Dashboard     │
│   Overview      │
└─────────────────┘
      │
      ├─────────────────────────────────────┬─────────────────────────────────┐
      │                                     │                                 │
      ↓                                     ↓                                 ↓
┌──────────────┐                  ┌──────────────┐               ┌──────────────┐
│ PRODUCTION   │                  │   REPORTS    │               │   PUMP       │
│   ENTRY      │                  │  GENERATION  │               │  SERVICE     │
└──────────────┘                  └──────────────┘               └──────────────┘
      │                                     │                           │
      ↓                                     ↓                           ↓
┌──────────────┐                  ┌──────────────┐               [Similar flow]
│ Fill Form:   │                  │ Select:      │
│ • Date       │                  │ • Party      │
│ • Party      │                  │ • Date Range │
│ • Grade      │                  │ • Report Type│
│ • Quantity   │                  └──────────────┘
│ • Rate       │                           │
│ • Vehicle    │                           ↓
└──────────────┘                  ┌──────────────────────────┐
      │                           │  Report Type Decision    │
      ↓                           └──────────────────────────┘
┌──────────────┐                           │
│ [SAVE]       │                           ├────────┬────────┬────────┐
│ Button       │                           │        │        │        │
└──────────────┘                           ↓        ↓        ↓        ↓
      │                              ┌────────┐┌────────┐┌────────┐┌────────┐
      ↓                              │ YOUR   ││ PARTY  ││VARIANCE││ OTHER  │
┌──────────────────┐                │PRODUC- ││STATEMT ││ANALYSIS││REPORTS │
│ Data Saved in:   │                │TION    ││        ││        ││        │
│ actual_production│                └────────┘└────────┘└────────┘└────────┘
└──────────────────┘                     │        │        │        │
      │                                  ↓        ↓        ↓        ↓
      ↓                              ┌───────────────────────────────┐
┌──────────────────┐                │  Generate & Display Report    │
│ Success Message  │                └───────────────────────────────┘
└──────────────────┘                             │
      │                                          ↓
      ↓                              ┌───────────────────────────────┐
┌──────────────────┐                │  Export Options:              │
│ Decision Point:  │                │  • PDF                        │
│ Party Document?  │                │  • Excel                      │
└──────────────────┘                │  • Email                      │
      │                              │  • Print                      │
      ├─────────────┬───────────     └───────────────────────────────┘
      │ NO          │ YES                         │
      ↓             ↓                             ↓
  [DONE]    ┌──────────────────┐               [END]
            │ Party Document   │
            │ Creation Form    │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Load Actual Data │
            │ (Read-only)      │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Edit Party Data: │
            │ • Grade          │
            │ • Rate           │
            │ • Reason         │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Variance Check   │
            │ & Validation     │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Approval Check   │
            │ (If required)    │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Data Saved in:   │
            │ party_documents  │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Update Link:     │
            │ actual_production│
            │ .has_party_doc   │
            └──────────────────┘
                    │
                    ↓
                [DONE]
```

---

## ✅ BLUEPRINT SUMMARY

### Documents Created:
```
✅ System Architecture Diagram
✅ Database ER Diagram (AutoCAD style)
✅ Screen Blueprint 1: Production Entry
✅ Screen Blueprint 2: Party Document Creation
✅ Screen Blueprint 3: Report Generation
✅ Report Layout: Print-ready view
✅ User Flow Diagram: Complete journey
```

### Design Specifications:
```
Screen Size:    1920px × 1080px (Full HD)
Grid System:    12-column responsive
Sidebar:        250px fixed width
Main Content:   calc(100% - 250px)
Font:           Sans-serif (UI), Monospace (Reports)
Colors:         Dark blue sidebar, White content area
Print:          A4 size (210mm × 297mm)
```

### Key Features:
```
✅ Responsive design
✅ Print-friendly layouts
✅ Clear visual hierarchy
✅ Access control indicators
✅ Real-time validation
✅ Professional look & feel
```

---

**Blueprint Status**: ✅ COMPLETE  
**Ready for**: Frontend Development  
**Next Step**: HTML/CSS Implementation

