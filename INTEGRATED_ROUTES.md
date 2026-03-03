# RMC ERP - Integrated Routes Documentation

## ✅ Integration Complete!

All HTML files from BLUEPRINTS folder have been successfully integrated into the Flask application.

## 📁 File Structure

```
SKCON RMC WEB APP/
├── app.py                  # Main Flask Application
├── templates/              # All HTML templates (copied from BLUEPRINTS)
│   ├── rmc_login_professional.html
│   ├── rmc_dashboard_blueprint.html
│   ├── rmc_cash_entries_view.html
│   ├── rmc_billing_entries_view.html
│   ├── party_master_blueprint.html
│   ├── party_ledger_unified.html
│   ├── rmc_material_master_blueprint.html
│   ├── rmc_vehicle_master_blueprint.html
│   ├── rmc_pump_master.html
│   ├── rmc_billing_entry_blueprint.html
│   ├── rmc_purchase_entry_blueprint.html
│   ├── rmc_payment_entry_blueprint.html
│   ├── rmc_diesel_management_blueprint.html
│   ├── rmc_pump_billing_service.html
│   └── rmc_pump_cash_service.html
├── static/                 # CSS, JS, Images
│   ├── css/
│   └── js/
└── BLUEPRINTS/            # Original HTML files (backup)
```

## 🌐 Available Routes

### Authentication
- **`/`** → Redirects to login
- **`/login`** → Login page (rmc_login_professional.html)
- **`/logout`** → Logout and clear session

### Main Dashboard
- **`/dashboard`** → Main Dashboard (rmc_dashboard_blueprint.html)

### Production Entries
- **`/cash-production`** → Cash Production Entry View (rmc_cash_entries_view.html)
- **`/billing-production`** → Billing Production Entry View (rmc_billing_entries_view.html)

### Reports & Ledgers
- **`/party-ledger`** → Party Ledger with GST (party_ledger_unified.html)
- **`/invoices`** → Invoices (placeholder)
- **`/challans`** → Challans (placeholder)
- **`/production-reports`** → Production Reports (placeholder)
- **`/sales-reports`** → Sales Reports (placeholder)

### Master Data Management
- **`/material-master`** → Material Master (rmc_material_master_blueprint.html)
- **`/party-master`** → Party/Customer Master (party_master_blueprint.html)
- **`/customers`** → Customers (same as party-master)
- **`/vehicle-master`** → Vehicle Master (rmc_vehicle_master_blueprint.html)
- **`/vehicles`** → Vehicles (same as vehicle-master)
- **`/pump-master`** → Pump Master (rmc_pump_master.html)

### Transaction Entries
- **`/billing-entry`** → RMC Billing Entry Form (rmc_billing_entry_blueprint.html)
- **`/purchase-entry`** → Purchase Entry Form (rmc_purchase_entry_blueprint.html)
- **`/payment-entry`** → Payment Entry Form (rmc_payment_entry_blueprint.html)

### Diesel Management
- **`/diesel-management`** → Diesel Management Dashboard (rmc_diesel_management_blueprint.html)
- **`/pump-billing`** → Pump Billing Service (rmc_pump_billing_service.html)
- **`/pump-cash`** → Pump Cash Service (rmc_pump_cash_service.html)

### API Endpoints
- **`/api/version`** → Get app version for cache busting
- **`/api/production-data`** → Production chart data (JSON)
- **`/api/grade-distribution`** → Grade distribution data (JSON)

### Static & Blueprints
- **`/static/<filename>`** → Serve static files (CSS, JS, images)
- **`/blueprints/<filename>`** → Direct access to BLUEPRINTS folder files

## 🚀 How to Run

1. **Start the application:**
   ```bash
   python app.py
   ```
   OR double-click `START_WEB_APP.bat`

2. **Open browser:**
   ```
   http://localhost:8080
   ```

3. **Login:**
   - Username: Any (e.g., "admin")
   - Password: Any (e.g., "admin")
   - Demo mode - accepts any credentials

## 🔧 Features

### ✅ Implemented
- Session-based authentication
- All HTML templates integrated
- Cache busting for development
- Aggressive no-cache headers
- Professional UI from blueprints
- Responsive design
- Modern card-based layouts

### 🎨 UI Features
- Professional color scheme
- Modern card layouts
- Interactive forms
- Data tables with search/filter
- Modal dialogs
- Dropdown menus
- Responsive sidebar navigation
- User profile dropdown
- Notification badges

## 📝 Notes

1. **Session Management:**
   - All routes check for `logged_in` session
   - Redirects to login if not authenticated
   - Session stores username and user data

2. **Template Data:**
   - Common data passed via `get_template_data()` function
   - Includes: plant, financial_year, current_date, user info, etc.

3. **Static Files:**
   - CSS files in `static/css/`
   - JavaScript files in `static/js/`
   - Images in `static/images/` (if needed)

4. **Development Mode:**
   - Debug mode enabled
   - Auto-reload on file changes
   - Aggressive cache prevention
   - Detailed error messages

## 🎯 Next Steps

1. **Database Integration:**
   - Add SQLite/PostgreSQL database
   - Create models for all entities
   - Implement CRUD operations

2. **API Development:**
   - Create REST APIs for data operations
   - Add data validation
   - Implement business logic

3. **Additional Features:**
   - Export to PDF/Excel
   - Advanced filtering
   - Real-time updates
   - Report generation
   - Print functionality

4. **Security:**
   - Implement proper authentication
   - Add password hashing
   - Role-based access control
   - CSRF protection

## 🐛 Troubleshooting

**Issue: Templates not loading**
- Check if `templates/` folder exists
- Verify HTML files are in templates folder
- Check file names match exactly

**Issue: Static files (CSS/JS) not loading**
- Verify `static/` folder structure
- Check browser console for 404 errors
- Clear browser cache (Ctrl+Shift+R)

**Issue: Session not persisting**
- Check if `app.secret_key` is set
- Clear browser cookies
- Restart Flask application

## 📞 Support

For issues or questions:
- Check BLUEPRINTS/README.md
- Review BLUEPRINTS/BLUEPRINT_GUIDE.md
- Check Flask documentation: https://flask.palletsprojects.com/

---

**Created:** January 23, 2026
**Last Updated:** January 23, 2026
**Version:** 1.0.0
