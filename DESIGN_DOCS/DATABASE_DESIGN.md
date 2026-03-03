# 🏗️ RMC PRODUCTION SYSTEM - COMPLETE DATABASE DESIGN

**Date**: 24-Jan-2026  
**For**: SKCON RMC Plant ERP  
**Purpose**: Dual-Rate Production & Party Management System

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [Table Relationships](#table-relationships)
4. [Sample Data](#sample-data)
5. [Key Features](#key-features)

---

## 🎯 OVERVIEW

### Problem Statement
RMC business mein parties ko:
- **Different grades** chahiye paper pe (Actual: M25, Document: M30)
- **Different rates** chahiye billing mein (Actual: ₹5,000, Document: ₹5,200)
- Lekin **payment actual rate pe** hi hota hai

### Solution
**TWO SEPARATE TABLES** - Data never mixes!
```
actual_production (YOUR TRUTH)
        ↓ linked by ID
party_documents (THEIR REQUEST)
```

---

## 🗄️ DATABASE SCHEMA

### 1️⃣ **PARTIES MASTER TABLE**

```sql
-- ════════════════════════════════════════════════════
-- PARTIES: Customer/Party Master Data
-- ════════════════════════════════════════════════════

CREATE TABLE parties (
    -- Primary Key
    party_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Basic Info
    party_code VARCHAR(20) UNIQUE NOT NULL,
    party_name VARCHAR(200) NOT NULL,
    party_type VARCHAR(20) DEFAULT 'Customer',  -- Customer, Contractor, Builder
    
    -- Contact Details
    contact_person VARCHAR(100),
    mobile VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    pincode VARCHAR(10),
    
    -- Business Details
    gst_no VARCHAR(20),
    pan_no VARCHAR(20),
    
    -- Special Settings (IMPORTANT!)
    allow_dual_rate BOOLEAN DEFAULT FALSE,        -- Can have different rates?
    allow_grade_change BOOLEAN DEFAULT FALSE,     -- Can show different grade?
    require_approval BOOLEAN DEFAULT TRUE,        -- Manager approval needed?
    
    -- Financial
    credit_limit DECIMAL(12,2) DEFAULT 0,
    credit_days INT DEFAULT 0,
    opening_balance DECIMAL(12,2) DEFAULT 0,
    balance_type VARCHAR(10) DEFAULT 'Dr',        -- Dr or Cr
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    risk_level VARCHAR(20) DEFAULT 'LOW',         -- LOW, MEDIUM, HIGH
    
    -- Audit
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_party_name (party_name),
    INDEX idx_party_code (party_code),
    INDEX idx_is_active (is_active)
);
```

---

### 2️⃣ **SITES MASTER TABLE**

```sql
-- ════════════════════════════════════════════════════
-- SITES: Delivery locations for parties
-- ════════════════════════════════════════════════════

CREATE TABLE sites (
    -- Primary Key
    site_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Basic Info
    site_code VARCHAR(20) UNIQUE NOT NULL,
    site_name VARCHAR(200) NOT NULL,
    party_id INT NOT NULL,
    
    -- Location
    address TEXT,
    city VARCHAR(100),
    pincode VARCHAR(10),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    distance_km DECIMAL(6,2),                     -- Distance from plant
    
    -- Contact
    site_incharge VARCHAR(100),
    site_mobile VARCHAR(15),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    project_start_date DATE,
    project_end_date DATE,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys & Indexes
    FOREIGN KEY (party_id) REFERENCES parties(party_id),
    INDEX idx_party_id (party_id),
    INDEX idx_site_name (site_name)
);
```

---

### 3️⃣ **GRADE MASTER TABLE**

```sql
-- ════════════════════════════════════════════════════
-- GRADES: Concrete grade master (M20, M25, M30, etc)
-- ════════════════════════════════════════════════════

CREATE TABLE grades (
    -- Primary Key
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Grade Info
    grade_code VARCHAR(10) UNIQUE NOT NULL,       -- M20, M25, M30, M35, M40
    grade_name VARCHAR(50) NOT NULL,              -- Standard M25 Grade
    
    -- Specifications
    cement_content DECIMAL(6,2),                  -- kg per CUM
    water_cement_ratio DECIMAL(5,3),
    slump_range VARCHAR(20),                      -- "75-100mm"
    compressive_strength INT,                     -- N/mm²
    
    -- Pricing
    base_rate DECIMAL(10,2),                      -- Default rate
    
    -- Mix Design
    mix_design_code VARCHAR(50),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_grade_code (grade_code)
);
```

---

### 4️⃣ **ACTUAL PRODUCTION TABLE** ⭐ (YOUR TRUTH)

```sql
-- ════════════════════════════════════════════════════
-- ACTUAL_PRODUCTION: Real production data (YOUR BOOKS)
-- This is your PURE data - NEVER gets mixed!
-- ════════════════════════════════════════════════════

CREATE TABLE actual_production (
    -- Primary Key
    production_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Document Info
    challan_no VARCHAR(20) UNIQUE NOT NULL,
    production_date DATE NOT NULL,
    production_time TIME,
    
    -- Party & Site
    party_id INT NOT NULL,
    site_id INT,
    
    -- ✅ ACTUAL SUPPLY (PURE DATA - NO MANIPULATION)
    actual_grade_id INT NOT NULL,
    actual_grade_code VARCHAR(10) NOT NULL,       -- M25 (denormalized for speed)
    actual_quantity DECIMAL(10,2) NOT NULL,       -- 10.00 CUM
    actual_rate DECIMAL(10,2) NOT NULL,           -- 5,000 per CUM
    actual_amount DECIMAL(10,2) NOT NULL,         -- 50,000
    
    -- GST Calculation (on actual amount)
    cgst_percentage DECIMAL(5,2) DEFAULT 9.00,
    sgst_percentage DECIMAL(5,2) DEFAULT 9.00,
    cgst_amount DECIMAL(10,2),
    sgst_amount DECIMAL(10,2),
    total_gst DECIMAL(10,2),
    total_amount DECIMAL(10,2),                   -- 59,000
    
    -- Delivery Details
    vehicle_no VARCHAR(20),
    driver_name VARCHAR(100),
    driver_mobile VARCHAR(15),
    
    -- Quality Control
    mix_design_code VARCHAR(50),
    cement_content DECIMAL(6,2),
    water_cement_ratio DECIMAL(5,3),
    slump_value INT,                              -- mm
    lab_test_no VARCHAR(50),
    
    -- Production Info
    batch_no VARCHAR(20),
    mixer_operator VARCHAR(100),
    plant_name VARCHAR(100) DEFAULT 'Plant A - XYZ',
    
    -- Status Tracking
    production_status VARCHAR(20) DEFAULT 'Completed',  -- Completed, Cancelled, Pending
    delivery_status VARCHAR(20) DEFAULT 'Delivered',    -- Delivered, In-Transit, Rejected
    payment_status VARCHAR(20) DEFAULT 'Pending',       -- Pending, Partial, Paid
    
    -- Link to party document (if exists)
    has_party_document BOOLEAN DEFAULT FALSE,
    party_document_count INT DEFAULT 0,
    
    -- Remarks
    remarks TEXT,
    internal_notes TEXT,                          -- For internal use only
    
    -- Audit Trail
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (party_id) REFERENCES parties(party_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (actual_grade_id) REFERENCES grades(grade_id),
    
    -- Indexes for Performance
    INDEX idx_production_date (production_date),
    INDEX idx_challan_no (challan_no),
    INDEX idx_party_id (party_id),
    INDEX idx_site_id (site_id),
    INDEX idx_date_party (production_date, party_id),
    INDEX idx_payment_status (payment_status)
);
```

---

### 5️⃣ **PARTY DOCUMENTS TABLE** ⭐ (THEIR REQUEST)

```sql
-- ════════════════════════════════════════════════════
-- PARTY_DOCUMENTS: Party requested documents (SEPARATE)
-- This stores what party wants on paper - SEPARATE from actual!
-- ════════════════════════════════════════════════════

CREATE TABLE party_documents (
    -- Primary Key
    document_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Link to Actual Production (IMPORTANT!)
    production_id INT NOT NULL,
    challan_no VARCHAR(20),                       -- Same as actual production
    
    -- Document Details
    document_type VARCHAR(50) DEFAULT 'Tax Invoice',  -- Tax Invoice, Delivery Note, Proforma
    invoice_no VARCHAR(20) UNIQUE,
    invoice_date DATE NOT NULL,
    
    -- Party Info
    party_id INT NOT NULL,
    site_id INT,
    
    -- 📄 PARTY REQUESTED DATA (SEPARATE - NO MIXING!)
    document_grade_id INT,
    document_grade_code VARCHAR(10),              -- M30 (party chahta hai)
    document_quantity DECIMAL(10,2),              -- Usually same as actual
    document_rate DECIMAL(10,2),                  -- 5,200 (party rate)
    document_amount DECIMAL(10,2),                -- 52,000
    
    -- GST (on document amount)
    document_cgst_percentage DECIMAL(5,2) DEFAULT 9.00,
    document_sgst_percentage DECIMAL(5,2) DEFAULT 9.00,
    document_cgst DECIMAL(10,2),
    document_sgst DECIMAL(10,2),
    document_total_gst DECIMAL(10,2),
    document_total DECIMAL(10,2),                 -- 61,360
    
    -- Variance Tracking (Auto-calculated)
    grade_different BOOLEAN DEFAULT FALSE,         -- Actual grade ≠ Document grade?
    rate_different BOOLEAN DEFAULT FALSE,          -- Actual rate ≠ Document rate?
    grade_variance VARCHAR(50),                    -- "M25 → M30"
    rate_variance DECIMAL(10,2),                   -- +200
    amount_variance DECIMAL(10,2),                 -- +2,000
    
    -- Authorization & Risk Management
    request_reason TEXT NOT NULL,                  -- Why different from actual?
    requested_by VARCHAR(100),                     -- Party person name
    requested_date DATE,
    
    approved_by VARCHAR(100),                      -- Your manager/admin
    approval_date DATE,
    approval_notes TEXT,
    
    written_agreement BOOLEAN DEFAULT FALSE,       -- Agreement received from party?
    agreement_file_path VARCHAR(500),              -- Scan of signed agreement
    liability_accepted_by VARCHAR(100),            -- Who accepts liability?
    
    -- Document Status
    document_status VARCHAR(20) DEFAULT 'Draft',   -- Draft, Approved, Issued, Cancelled
    issued_to_party BOOLEAN DEFAULT FALSE,
    issue_date DATE,
    issue_method VARCHAR(50),                      -- Email, Print, WhatsApp
    
    -- Printing
    print_count INT DEFAULT 0,
    last_printed_at TIMESTAMP,
    
    -- Risk Level
    risk_level VARCHAR(20) DEFAULT 'MEDIUM',       -- LOW, MEDIUM, HIGH
    
    -- Remarks
    party_remarks TEXT,
    internal_notes TEXT,
    
    -- Audit Trail
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (production_id) REFERENCES actual_production(production_id),
    FOREIGN KEY (party_id) REFERENCES parties(party_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (document_grade_id) REFERENCES grades(grade_id),
    
    -- Indexes
    INDEX idx_production_id (production_id),
    INDEX idx_invoice_no (invoice_no),
    INDEX idx_party_id (party_id),
    INDEX idx_invoice_date (invoice_date),
    INDEX idx_document_status (document_status),
    INDEX idx_variance (grade_different, rate_different)
);
```

---

### 6️⃣ **PUMP SERVICE TABLE**

```sql
-- ════════════════════════════════════════════════════
-- PUMP_SERVICES: Concrete pump service records
-- ════════════════════════════════════════════════════

CREATE TABLE pump_services (
    -- Primary Key
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Service Details
    service_no VARCHAR(20) UNIQUE NOT NULL,
    service_date DATE NOT NULL,
    
    -- Party & Site
    party_id INT NOT NULL,
    site_id INT,
    
    -- Pump Details
    pump_type VARCHAR(20),                        -- 28M, 32M, 36M, Static
    pump_number VARCHAR(20),
    
    -- Time Tracking
    start_time TIME,
    end_time TIME,
    total_hours DECIMAL(5,2),                     -- Auto-calculated
    break_hours DECIMAL(5,2) DEFAULT 0,
    billable_hours DECIMAL(5,2),
    
    -- Rates
    rate_per_hour DECIMAL(10,2),
    amount DECIMAL(10,2),
    
    -- GST
    gst_percentage DECIMAL(5,2) DEFAULT 18.00,
    gst_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    
    -- Operator
    operator_name VARCHAR(100),
    operator_mobile VARCHAR(15),
    
    -- Status
    service_status VARCHAR(20) DEFAULT 'Completed',
    payment_status VARCHAR(20) DEFAULT 'Pending',
    
    -- Remarks
    remarks TEXT,
    
    -- Audit
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (party_id) REFERENCES parties(party_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    
    -- Indexes
    INDEX idx_service_date (service_date),
    INDEX idx_party_id (party_id)
);
```

---

### 7️⃣ **USERS TABLE** (For Access Control)

```sql
-- ════════════════════════════════════════════════════
-- USERS: System users with role-based access
-- ════════════════════════════════════════════════════

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    
    email VARCHAR(100),
    mobile VARCHAR(15),
    
    -- Role & Permissions
    role VARCHAR(50) NOT NULL,                     -- Admin, Manager, Operator, Accountant
    
    -- Access Controls
    can_create_production BOOLEAN DEFAULT FALSE,
    can_create_party_doc BOOLEAN DEFAULT FALSE,
    can_approve_dual_rate BOOLEAN DEFAULT FALSE,
    can_view_variance BOOLEAN DEFAULT FALSE,       -- Can see actual vs document?
    can_export_reports BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_role (role)
);
```

---

## 🔗 TABLE RELATIONSHIPS

```
┌──────────────┐
│   PARTIES    │──────┐
└──────────────┘      │
       │              │
       │ has many     │
       ↓              │
┌──────────────┐      │
│    SITES     │      │
└──────────────┘      │
                      │
┌──────────────┐      │ has many
│    GRADES    │      │
└──────────────┘      │
       │              │
       │              │
       ↓              ↓
┌─────────────────────────────────┐
│   ACTUAL_PRODUCTION (Table 1)   │ ⭐ YOUR TRUTH
└─────────────────────────────────┘
       │
       │ has zero or one
       │ (optional)
       ↓
┌─────────────────────────────────┐
│   PARTY_DOCUMENTS (Table 2)     │ ⭐ THEIR REQUEST
└─────────────────────────────────┘

┌──────────────┐
│ PUMP_SERVICES│ (Independent)
└──────────────┘

┌──────────────┐
│    USERS     │ (System users)
└──────────────┘
```

### Key Relationships:

1. **ONE Production → ZERO or ONE Party Document**
   - Not all productions need party documents
   - Only create when party requests different data

2. **ONE Party → MANY Productions**
   - Party can have multiple deliveries

3. **ONE Site → MANY Productions**
   - Same site gets multiple deliveries

4. **ONE Grade → MANY Productions**
   - Same grade used in multiple productions

---

## 📊 SAMPLE DATA

### Insert Sample Parties

```sql
INSERT INTO parties (party_code, party_name, mobile, gst_no, allow_dual_rate, allow_grade_change) VALUES
('P001', 'ABC Builders Pvt Ltd', '9876543210', '27AAAAA1234A1Z5', TRUE, TRUE),
('P002', 'XYZ Construction', '9876543211', '27BBBBB5678B1Z5', FALSE, FALSE),
('P003', 'PQR Developers', '9876543212', '27CCCCC9012C1Z5', TRUE, FALSE);
```

### Insert Sample Grades

```sql
INSERT INTO grades (grade_code, grade_name, cement_content, base_rate, is_active) VALUES
('M20', 'Standard M20 Grade', 300, 4500, TRUE),
('M25', 'Standard M25 Grade', 350, 5000, TRUE),
('M30', 'High Strength M30', 380, 6000, TRUE),
('M35', 'High Strength M35', 400, 7000, TRUE),
('M40', 'Ultra High Strength M40', 420, 8000, TRUE);
```

### Insert Sample Production

```sql
-- Actual Production (YOUR TRUTH)
INSERT INTO actual_production (
    challan_no, production_date, production_time,
    party_id, actual_grade_id, actual_grade_code,
    actual_quantity, actual_rate, actual_amount,
    cgst_amount, sgst_amount, total_gst, total_amount,
    vehicle_no, driver_name,
    production_status, delivery_status,
    created_by
) VALUES (
    'CH-001', '2026-01-05', '10:30:00',
    1, 2, 'M25',
    10.00, 5000.00, 50000.00,
    4500.00, 4500.00, 9000.00, 59000.00,
    'MH12AB1234', 'Ram Kumar',
    'Completed', 'Delivered',
    'System'
);

-- Party Document (THEIR REQUEST - Different grade & rate)
INSERT INTO party_documents (
    production_id, challan_no,
    document_type, invoice_no, invoice_date,
    party_id,
    document_grade_id, document_grade_code,
    document_quantity, document_rate, document_amount,
    document_cgst, document_sgst, document_total_gst, document_total,
    grade_different, rate_different,
    grade_variance, rate_variance, amount_variance,
    request_reason, requested_by, approved_by, approval_date,
    document_status, risk_level,
    created_by
) VALUES (
    1, 'CH-001',
    'Tax Invoice', 'INV-001', '2026-01-05',
    1,
    3, 'M30',
    10.00, 5200.00, 52000.00,
    4680.00, 4680.00, 9360.00, 61360.00,
    TRUE, TRUE,
    'M25 → M30', 200.00, 2000.00,
    'Party requested M30 grade document for their client presentation',
    'Ramesh (ABC)', 'Manager', '2026-01-05',
    'Approved', 'MEDIUM',
    'System'
);
```

---

## ✅ KEY FEATURES OF THIS DESIGN

### 1. **Data Integrity** ✅
- Actual production data NEVER changes
- Party documents stored separately
- No mixing of real and document data

### 2. **Flexibility** ✅
- Can create party document only when needed
- Can have multiple document versions for same production
- Easy to modify party document without affecting actual data

### 3. **Audit Trail** ✅
- Complete history of who requested what
- Approval chain maintained
- Timestamps for all changes

### 4. **Reporting** ✅
- Simple queries for your reports (actual_production table)
- Simple queries for party reports (party_documents table)
- Join both for variance analysis

### 5. **Security** ✅
- Role-based access control
- Variance visible only to authorized users
- Approval required for dual rates

### 6. **Performance** ✅
- Proper indexes on all search columns
- Denormalized grade_code for faster queries
- Separate tables = faster queries

---

## 🎯 NEXT STEPS

1. ✅ Database schema created
2. ⏳ Create SQL queries for reports
3. ⏳ Design UI screens
4. ⏳ Create business logic/rules
5. ⏳ Implement in Flask application

---

**Design Status**: ✅ COMPLETE & READY TO IMPLEMENT  
**Complexity**: Simple & Clean  
**Maintenance**: Easy to understand and modify
