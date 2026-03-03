# Read file
with open('rmc_erp_full_layout.html.backup', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace line 689 (index 688) and 690
lines[688] = '            <div class="nav-section">\n'
lines.insert(689, '                <div class="nav-section-title">Reports</div>\n')
lines[690] = '                <a href="/all-reports" class="nav-item">\n'
lines[691] = '                    <span class="nav-icon"></span>\n'

# Write file
with open('rmc_erp_full_layout.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print(' Reports section fixed!')
