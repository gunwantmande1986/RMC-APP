# 🌐 SKCON RMC - Web Application

Modern web-based ERP system for RMC (Ready Mix Concrete) plant management.

## ✅ STATUS: FULLY INTEGRATED (January 23, 2026)

All HTML blueprints have been successfully integrated into Flask application with proper routing!

## 📁 Project Structure

```
SKCON RMC WEB APP/
├── BLUEPRINTS/              # Original HTML blueprints (backup)
│   ├── rmc_erp_full_layout.html
│   ├── rmc_dashboard_blueprint.html
│   ├── rmc_login_professional.html
│   ├── party_master_blueprint.html
│   ├── rmc_material_master_blueprint.html
│   ├── rmc_vehicle_master_blueprint.html
│   ├── rmc_billing_entry_blueprint.html
│   ├── rmc_purchase_entry_blueprint.html
│   ├── rmc_diesel_management_blueprint.html
│   └── ... (26+ HTML files)
├── templates/               # ✅ Flask templates (copied from BLUEPRINTS)
│   ├── rmc_login_professional.html
│   ├── rmc_dashboard_blueprint.html
│   ├── party_master_blueprint.html
│   ├── rmc_material_master_blueprint.html
│   └── ... (all HTML files)
├── static/                  # CSS, JS, images
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── login.css
│   │   └── erp_layout.css
│   └── js/
├── app.py                   # ✅ Main Flask app (fully integrated)
├── requirements.txt         # Python dependencies
├── START_WEB_APP.bat       # Quick start script
├── INTEGRATED_ROUTES.md    # ✅ Complete route documentation
├── INTEGRATION_SUCCESS.md  # ✅ Integration summary
└── README.md               # This file
```

## 🚀 Quick Start

### Method 1: Double-Click (Easiest)
```
1. Double-click START_WEB_APP.bat
2. Browser will open automatically
3. Login with any credentials
```

### Method 2: Command Line
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python app.py
```

### 3. Open Browser
Navigate to: **http://localhost:8080**

### 4. Login
- Username: Any (e.g., "admin")
- Password: Any (e.g., "admin")
- Demo mode - accepts any credentials

## 📋 Integrated Features

### ✅ Authentication
- Professional login page
- Session management
- Secure logout

### ✅ Dashboard & Reports
- `/dashboard` - Main dashboard with charts
- `/party-ledger` - Party ledger with GST
- `/production-reports` - Production analytics
- `/sales-reports` - Sales reports

### ✅ Production Management
- `/cash-production` - Cash production entries view
- `/billing-production` - Billing production entries view

### ✅ Master Data Management
- `/material-master` - Material master with categories
- `/party-master` - Customer/Supplier master
- `/vehicle-master` - Vehicle registration & management
- `/pump-master` - Pump master data

### ✅ Transaction Entries
- `/billing-entry` - Complete billing entry form
- `/purchase-entry` - Purchase entry form
- `/payment-entry` - Payment entry form

### ✅ Diesel Management Module
- `/diesel-management` - Diesel management dashboard
- `/pump-billing` - Pump billing service
- `/pump-cash` - Pump cash service
- ✅ Multi-user support (planned)
- ✅ Real-time updates (planned)

## 🎨 Design Philosophy

This web app uses the **blueprint designs** from the `BLUEPRINTS/` folder as the foundation for all UI components.

## 📝 Development Status

🔨 **In Active Development**

This is a new web application being built alongside the existing desktop application.

---

**Desktop Application:** Located in `SKCON RMC ORIGINAL FILE PYTHON/`  
**Web Application:** This folder (separate development)

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (to be integrated)
- **UI Design:** Professional blueprint-inspired theme

## 📞 Support

For any issues or questions, contact the development team.

---

**Last Updated:** January 21, 2026
