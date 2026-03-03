# Read original backup
with open('rmc_erp_full_layout.html.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Define old content (the malformed section)
old = '''            <div class="nav-section">
                <a href="/all-reports" class="nav-item" target="_blank">
                    <span class="nav-icon"></span>
                    <span class="nav-text">All Reports</span>
                    <span style="margin-left: auto; font-size: 10px; color: #00FF88;"> NEW</span>
                </a>
                <a href="#" class="nav-item" onclick="loadModule('reports-production')">
                    <span class="nav-icon"></span>
                    <span class="nav-text">Sales Reports</span>
                </a>'''

# Define new content (properly formatted)
new = '''            <div class="nav-section">
                <div class="nav-section-title">Reports</div>
                <a href="/all-reports" class="nav-item">
                    <span class="nav-icon"></span>
                    <span class="nav-text">All Reports</span>
                    <span style="margin-left: auto; font-size: 10px; color: #00FF88;"> NEW</span>
                </a>
                <a href="/production-reports" class="nav-item">
                    <span class="nav-icon"></span>
                    <span class="nav-text">Production Reports</span>
                </a>
                <a href="/sales-reports" class="nav-item">
                    <span class="nav-icon"></span>
                    <span class="nav-text">Sales Reports</span>
                </a>'''

# Replace
content = content.replace(old, new)

# Write
with open('rmc_erp_full_layout.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Complete Reports section with all 3 items added!')
