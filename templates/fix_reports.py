with open('rmc_erp_full_layout.html.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Reports section title
old1 = '''            <div class="nav-section">
                <a href="/all-reports"'''
new1 = '''            <div class="nav-section">
                <div class="nav-section-title">Reports</div>
                <a href="/all-reports"'''

# Add icon for All Reports
old2 = '''<a href="/all-reports" class="nav-item" target="_blank">
                    <span class="nav-icon"></span>'''
new2 = '''<a href="/all-reports" class="nav-item" target="_blank">
                    <span class="nav-icon"></span>'''

content = content.replace(old1, new1)
content = content.replace(old2, new2)

with open('rmc_erp_full_layout.html', 'w', encoding='utf-8') as f:
    f.write(content)
    
print(' Reports section fixed!')
