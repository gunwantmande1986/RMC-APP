# 🔵 RMC ERP BLUEPRINT - OFFICIAL DESIGN REFERENCE

**Date Created:** 20-Jan-2026  
**Status:** FINAL - LOCKED  
**Purpose:** Single Source of Truth for UI/UX Design

---

## ⚠️ CRITICAL RULES

### 🔴 MANDATORY COMPLIANCE:

1. **This blueprint file is the ONLY design reference**
2. **NO design improvisation is allowed**
3. **Every screen must match this blueprint exactly**
4. **Pixel-perfect implementation required**
5. **Changes require written approval only**

---

## 📁 BLUEPRINT FILE LOCATION

```
📂 BLUEPRINTS/
   └── rmc_blueprint_exact.html (FINAL - 1813 lines)
```

**File Size:** ~70 KB  
**Total Lines:** 1813  
**Language:** HTML5 + CSS3 + Vanilla JavaScript

---

## 🎨 LOCKED DESIGN VALUES

### Header
- **Height:** 55px (fixed)
- **Background:** #0f1e32
- **Border:** 2px solid #4a6b8a

### Form Labels
- **Font Size:** 11px
- **Font Weight:** 400 (normal), 600 (section headers)
- **Color:** #c8d9f0

### Form Inputs
- **Height:** 32px (fixed)
- **Padding:** 6px 10px
- **Border:** 1px solid #4a6b8a
- **Background:** rgba(26, 41, 66, 0.3)
- **Font Size:** 12px

### Buttons
- **Min Height:** 32px
- **Padding:** 8px 16px
- **Font Size:** 11px
- **Font Weight:** 600

### Color Palette (LOCKED)
```css
Primary Background: #0a1628
Secondary Background: #1a2942
Primary Text: #c8d9f0
Success/Green: #90d090
Info/Blue: #8aa4c4
Danger/Red: #d08090
Border: #4a6b8a
```

---

## 📐 LAYOUT STRUCTURE

```
┌─────────────────────────────────────────────────────┐
│ HEADER (55px)                                       │
│ - Logo, Title, Buttons                              │
├─────────────────────────────────────────────────────┤
│ INFO BAR (Optional - 20px)                          │
├─────────────────────────────────────────────────────┤
│ MAIN CONTENT AREA                                   │
│                                                     │
│ ┌─────────────────┐ ┌────────────────────────────┐│
│ │  LEFT SECTION   │ │   RIGHT SECTION            ││
│ │                 │ │                            ││
│ │ - Production    │ │ - Actual Production        ││
│ │   Details       │ │ - Challan Details          ││
│ │ - Party Info    │ │ - Quantity Difference      ││
│ │ - Challan No    │ │ - Material Consumption     ││
│ │ - Vehicle Info  │ │                            ││
│ └─────────────────┘ └────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

---

## 🔧 FORM SECTIONS (Exact Order)

### LEFT COLUMN:
1. **Production Date** (Required *)
2. **Plant Name** (Required *)
3. **Time**
4. **Production Type** (Radio: RMC / Cement)
5. **Party Name** (Required *, with + button)
6. **Sub Party** (Optional, with + button)
7. **Site/Location** (Required *, with + button)
8. **Challan No** (Required *)
9. **Vehicle No** (Required *, with + button)
10. **Driver Name** (Optional, with + button)
11. **Driver Optional** (Checkbox)

### RIGHT COLUMN:
1. **Actual Production Section** (Green header)
   - Actual Grade (Required *, dropdown)
   - Actual Quantity CUM (Required *, number input)

2. **Challan Details Section** (Blue header)
   - Challan Grade (Required *, dropdown)
   - Challan Quantity CUM (Required *, number input)

3. **Quantity Difference Box**
   - Shows: Actual - Challan
   - Color: Green if 0, Yellow if difference
   - Position: Right-aligned, "Adjust Billing" in top-right

4. **Material Consumption Table**
   - Cement, Admixture, Fly Ash, Aggregates, Water

---

## 🚫 BLUEPRINT-ONLY ELEMENTS (Remove in Production)

These are for design reference only - **DO NOT include in production:**

```css
❌ .blueprint-container::before (Grid background)
❌ .corner (Corner marks: TL, TR, BL, BR)
❌ .dimension (Dimension labels)
❌ Any "BLUEPRINT" text or watermarks
```

---

## ✅ KEEP IN PRODUCTION

```css
✅ All .form-label styles
✅ All .form-input styles
✅ All .btn-* button variants
✅ Header structure & styling
✅ Section layout & spacing
✅ Color palette (exact hex codes)
✅ All JavaScript functions
✅ Quantity difference calculation
✅ Material table structure
```

---

## 🔌 BACKEND INTEGRATION MAPPING

### Form Fields → Python Variables:

```python
# Production Details
prod_date = request.form.get('production_date')
plant_name = request.form.get('plant_name')
prod_time = request.form.get('production_time')
prod_type = request.form.get('production_type')  # 'RMC' or 'Cement'

# Party Information
party_name = request.form.get('party_name')
sub_party = request.form.get('sub_party')
site_location = request.form.get('site_location')

# Challan & Vehicle
challan_no = request.form.get('challan_no')
vehicle_no = request.form.get('vehicle_no')
driver_name = request.form.get('driver_name')
driver_optional = request.form.get('driver_optional')  # Boolean

# Production Quantities
actual_grade = request.form.get('actual_grade')
actual_qty = float(request.form.get('actual_qty'))
challan_grade = request.form.get('challan_grade')
challan_qty = float(request.form.get('challan_qty'))

# Calculated Fields
qty_difference = actual_qty - challan_qty
adjust_billing = request.form.get('adjust_billing')  # 'actual' or 'challan'
```

---

## 📊 VALIDATION RULES

### Required Fields (marked with *):
- Production Date
- Plant Name
- Party Name
- Site/Location
- Challan No
- Vehicle No
- Actual Grade
- Actual Quantity
- Challan Grade
- Challan Quantity

### Optional Fields:
- Time (defaults to current time)
- Sub Party
- Driver Name (if "Driver Optional" checked)

### Data Types:
- Quantities: `float` (2 decimal places)
- Dates: `DD-MM-YYYY` format
- Time: `HH:MM` format (24-hour)

---

## 🎯 JAVASCRIPT FUNCTIONS

### calculateDifference()
```javascript
// Calculates: Actual Qty - Challan Qty
// Updates difference display
// Changes color based on value (green/yellow/red)
```

### Form Validation
```javascript
// Validates all required fields before submit
// Shows error messages for missing data
// Prevents submission if validation fails
```

---

## 📸 VISUAL REFERENCE

**To verify your implementation:**

1. Open `rmc_blueprint_exact.html` in browser
2. Take screenshot of your developed screen
3. Place side-by-side for pixel comparison
4. Check:
   - ✅ Section heights match
   - ✅ Label sizes match
   - ✅ Input heights match
   - ✅ Colors match (use color picker)
   - ✅ Spacing matches
   - ✅ Button sizes match

---

## 🔒 VERSION CONTROL

**Blueprint Version:** 1.0 FINAL  
**Last Modified:** 20-Jan-2026 09:00 AM  
**Change History:** None (Initial Release)

### Change Approval Process:
1. Any design change requires written justification
2. Must be approved by project owner
3. Blueprint file must be updated first
4. Version number incremented
5. All screens re-verified

---

## 📞 CONTACT & CLARIFICATION

**For Design Questions:**
- Refer to this blueprint file ONLY
- Do NOT make assumptions
- Do NOT "improve" the design
- Ask for clarification if unclear

**Design Owner:** Gunvant  
**Project:** SKCON RMC ERP System

---

## ⚠️ FINAL WARNING

**"Kuch bhi banane" se pehle yeh samajh lo:**

❌ **WRONG APPROACH:**
- "Main isse thoda modern bana deta hoon"
- "Yeh color zyada better lagega"
- "Spacing thodi zyada kar deta hoon"

✅ **CORRECT APPROACH:**
- "Blueprint mein exactly kya hai?"
- "Kya mera screen blueprint se match kar raha hai?"
- "Kya koi difference hai? Fix karna padega."

---

## 📋 ACCEPTANCE CHECKLIST

Before marking any screen as "complete":

- [ ] Blueprint file opened side-by-side
- [ ] All sections present in correct order
- [ ] Header height = 55px
- [ ] Label font size = 11px
- [ ] Input height = 32px
- [ ] Button height = 32px
- [ ] Colors match exactly (hex codes)
- [ ] Spacing matches (use browser inspect)
- [ ] All required fields marked with *
- [ ] All optional fields clearly indicated
- [ ] JavaScript functions working
- [ ] Form validation working
- [ ] No design elements added/removed
- [ ] Screenshot comparison passed

---

**🎯 Remember: BLUEPRINT IS LAW. NO EXCEPTIONS.**

---

_This document is part of the SKCON RMC ERP official design system._  
_Last Updated: 20-Jan-2026_
