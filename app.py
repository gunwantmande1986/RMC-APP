# RMC ERP Web Application - Complete Flask App
# Uses the exact blueprint design from BLUEPRINTS folder

from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_from_directory, make_response
from datetime import datetime, timezone
import sys
import os

# Setup paths
sys.path.insert(0, os.path.dirname(__file__))

# 🔥 VERSION FOR CACHE BUSTING - Changes on every restart
APP_VERSION = str(datetime.now().timestamp()).replace('.', '')

# Create Flask app
app = Flask(__name__,
           template_folder='templates',
           static_folder='static')
app.secret_key = 'skcon-rmc-secret-key-2026-blueprint'

# 🔥 DISABLE CACHING FOR DEVELOPMENT
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_no_cache_headers(response):
    """AGGRESSIVE cache prevention for development"""
    # Prevent all caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Additional aggressive headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Vary'] = '*'
    
    # Force revalidation (using timezone-aware datetime)
    response.headers['Last-Modified'] = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response.headers['ETag'] = str(datetime.now(timezone.utc).timestamp())
    
    return response

# Helper function to get common template data
def get_template_data(active_page='dashboard'):
    return {
        'plant': 'Plant A - XYZ',
        'financial_year': '2025-26',
        'current_date': datetime.now().strftime('%d-%m-%Y'),
        'user_name': session.get('username', 'Gunvant Admin'),
        'user_initials': session.get('username', 'Gunvant Admin')[:2].upper(),
        'user_role': 'Super Administrator',
        'pending_invoices': '12',
        'active_page': active_page
    }

# Routes
@app.route('/')
def index():
    # Redirect to login directly
    return redirect(url_for('login'))

@app.route('/app')
def app_redirect():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple demo authentication
        if username and password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('rmc_login_professional.html', error='Invalid credentials')
    
    return render_template('rmc_login_professional.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # DEBUG - Print template path
    template_path = os.path.join(app.template_folder, 'rmc_erp_full_layout.html')
    print(f"🔥🔥🔥 SERVING TEMPLATE FROM: {template_path}")
    print(f"🔥🔥🔥 FILE EXISTS: {os.path.exists(template_path)}")
    
    data = get_template_data('dashboard')
    # Force fresh load with timestamp
    response = make_response(render_template('rmc_erp_full_layout.html', **data))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/cash-production')
def cash_production():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('cash_production')
    # Placeholder for now - will add actual form later
    return render_template('erp_dashboard.html', **data)

@app.route('/billing-production')
def billing_production():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('billing_production')
    return render_template('erp_dashboard.html', **data)

@app.route('/invoices')
def invoices():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('invoices')
    return render_template('erp_dashboard.html', **data)

@app.route('/challans')
def challans():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('challans')
    return render_template('erp_dashboard.html', **data)

@app.route('/production-reports')
def production_reports():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('production_reports')
    return render_template('rmc_reports_module.html', **data)

@app.route('/sales-reports')
def sales_reports():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('sales_reports')
    return render_template('rmc_reports_module.html', **data)

@app.route('/all-reports')
def all_reports():
    """All Reports - Comprehensive Reports System"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('all_reports')
    return render_template('rmc_reports_comprehensive.html', **data)

@app.route('/reports')
def reports():
    """Complete Reports Module"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('reports')
    return render_template('rmc_reports_module.html', **data)

@app.route('/reports-blueprint')
def reports_blueprint():
    """Reports Blueprint Design - Dark Navy Theme"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template('rmc_reports_blueprint.html')

@app.route('/party-ledger')
def party_ledger():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Serve the UNIFIED Party Ledger with GST, Totals, and Professional UI
    return render_template('party_ledger_unified.html')

@app.route('/material-master')
def material_master():
    """Material Master - Complete Inventory Management"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('material_master')
    return render_template('rmc_material_master.html', **data)

@app.route('/material-stock')
def material_stock():
    """Material Stock Report - Current Inventory Status"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('material_stock')
    return render_template('rmc_material_stock.html', **data)

@app.route('/material-consumption')
def material_consumption():
    """Material Consumption Report - Usage Analysis"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('material_consumption')
    return render_template('rmc_material_consumption.html', **data)

@app.route('/customers')
def customers():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('customers')
    return render_template('erp_dashboard.html', **data)

@app.route('/sites')
def sites():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('sites')
    return render_template('erp_dashboard.html', **data)

@app.route('/vehicles')
def vehicles():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('vehicles')
    return render_template('erp_dashboard.html', **data)

@app.route('/settings')
def settings():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('settings')
    return render_template('erp_dashboard.html', **data)

@app.route('/erp')
def erp_full_layout():
    """Main ERP Full Layout Page"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('dashboard')
    return render_template('rmc_erp_full_layout.html', **data)

@app.route('/opening-balance')
def opening_balance():
    """Opening Balance Entry System for Parties & Suppliers"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = get_template_data('opening_balance')
    return render_template('rmc_opening_balance_entry.html', **data)

@app.route('/erp-complete')
def erp_complete():
    """Complete Professional ERP System - SAP/Tally Style"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template('rmc_erp_professional_complete.html')

# API Endpoints for data (future use)
@app.route('/api/version')
def api_version():
    """Return current app version for cache busting"""
    return jsonify({'version': APP_VERSION})

@app.route('/api/production-data')
def api_production_data():
    import json
    data = {
        'labels': ['14-Jan', '15-Jan', '16-Jan', '17-Jan', '18-Jan', '19-Jan', '20-Jan'],
        'values': [220, 245, 210, 265, 240, 250, 245]
    }
    return jsonify(data)

@app.route('/api/grade-distribution')
def api_grade_distribution():
    import json
    data = {
        'labels': ['M20', 'M25', 'M30', 'M35', 'M40'],
        'values': [30, 25, 20, 15, 10]
    }
    return jsonify(data)

# Serve Blueprint HTML files directly
@app.route('/<path:filename>')
def serve_blueprints(filename):
    """Serve HTML files - TEMPLATES FIRST, then BLUEPRINTS"""
    
    if filename.endswith('.html'):
        # 🔥 PRIORITY 1: Check templates folder FIRST
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        template_file = os.path.join(templates_path, filename)
        if os.path.exists(template_file):
            print(f"🔥🔥🔥 SERVING FROM TEMPLATES: {template_file}")
            return send_from_directory(templates_path, filename)
        
        # PRIORITY 2: Try local BLUEPRINTS folder
        local_blueprints = os.path.join(os.path.dirname(__file__), 'BLUEPRINTS')
        if os.path.exists(os.path.join(local_blueprints, filename)):
            print(f"📋 Serving from local BLUEPRINTS: {filename}")
            return send_from_directory(local_blueprints, filename)
        
        # PRIORITY 3: Try original BLUEPRINTS folder
        original_blueprints = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'SKCON RMC ORIGINAL FILE PYTHON',
            'BLUEPRINTS'
        )
        file_path = os.path.join(original_blueprints, filename)
        if os.path.exists(file_path):
            print(f"📋 Serving from original BLUEPRINTS: {filename}")
            return send_from_directory(original_blueprints, filename)
    
    # For non-HTML files, try static folder
    try:
        return send_from_directory('static', filename)
    except:
        return "File not found", 404

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 RMC PLANT ERP - Professional Web Application")
    print("=" * 70)
    print("\n✅ Using EXACT Blueprint Design from BLUEPRINTS folder!")
    print(f"📍 Open browser at: http://localhost:8080")
    print(f"🔐 Login with any username/password for demo")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=8080, debug=True)


