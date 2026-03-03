# PowerShell script to fix edit button functionality
$filePath = "rmc_material_master_blueprint.html"

# Read the file with UTF8 encoding
$content = Get-Content $filePath -Raw -Encoding UTF8

# Define the old code block to replace
$oldCode = @"
            } else {
                alert(``✅ Inward Entry Updated!\n\n� Date: `${formattedDate}\n🏢 Party: `${party}\n� Material: `${materialName}\n📊 Quantity: `${quantity} `${unit}\n\n✅ Changes saved successfully!``);
            }
"@

# Define the new code block
$newCode = @"
            } else {
                // Edit existing entry
                const tbody = document.getElementById('materialsTableBody');
                const rows = tbody.getElementsByTagName('tr');
                const formattedDate = new Date(date).toLocaleDateString('en-IN');
                
                // Find the row to update by visible row number
                let targetRow = null;
                let visibleCount = 0;
                
                for (let i = 0; i < rows.length; i++) {
                    if (rows[i].style.display !== 'none') {
                        visibleCount++;
                        if (visibleCount === editingMaterialId) {
                            targetRow = rows[i];
                            break;
                        }
                    }
                }
                
                if (targetRow) {
                    const categoryBadge = getCategoryBadge(category);
                    
                    // Update all cells in the row
                    targetRow.cells[1].textContent = formattedDate;
                    targetRow.cells[1].style.fontWeight = '600';
                    
                    targetRow.cells[2].textContent = party;
                    targetRow.cells[2].style.fontWeight = '600';
                    
                    targetRow.cells[3].textContent = plant;
                    targetRow.cells[3].style.color = '#00d9ff';
                    targetRow.cells[3].style.fontWeight = '600';
                    
                    targetRow.cells[4].textContent = challan;
                    
                    targetRow.cells[5].textContent = materialName;
                    targetRow.cells[5].style.fontWeight = '600';
                    
                    targetRow.cells[6].innerHTML = categoryBadge;
                    
                    targetRow.cells[7].textContent = ``${quantity} ${unit}``;
                    targetRow.cells[7].style.fontWeight = '600';
                    targetRow.cells[7].style.color = '#90d090';
                    
                    targetRow.cells[8].textContent = ``₹ ${parseFloat(rate).toFixed(2)}``;
                    
                    targetRow.cells[9].textContent = ``₹ ${parseFloat(amount).toFixed(2)}``;
                    targetRow.cells[9].style.fontWeight = '600';
                    targetRow.cells[9].style.color = '#90d090';
                    
                    alert(``✅ Inward Entry Updated!\n\n📅 Date: ${formattedDate}\n🏢 Party: ${party}\n🏭 Plant: ${plant}\n📋 Challan: ${challan}\n📦 Material: ${materialName}\n📊 Quantity: ${quantity} ${unit}\n💰 Amount: ₹${parseFloat(amount).toFixed(2)}\n\n✅ Changes saved successfully!``);
                }
            }
"@

# Try to find and replace using regex to handle variations
$pattern = [regex]::Escape("} else {") + "[\s\S]*?" + [regex]::Escape("alert(") + "[\s\S]*?" + [regex]::Escape("Inward Entry Updated") + "[\s\S]*?" + [regex]::Escape("});") + "\s+" + [regex]::Escape("}")

if ($content -match $pattern) {
    Write-Host "Found the pattern - attempting replacement"
    $content = $content -replace $pattern, $newCode
    $content | Set-Content $filePath -Encoding UTF8 -NoNewline
    Write-Host "✅ Replacement complete!"
} else {
    Write-Host "❌ Pattern not found - trying line-based approach"
    
    # Alternative: Replace based on line numbers
    $lines = Get-Content $filePath -Encoding UTF8
    
    # Find line 1408-1410 and replace
    $startLine = 1407  # 0-indexed
    $endLine = 1409
    
    if ($lines[$startLine] -match "} else {") {
        Write-Host "Found else block at line $($startLine + 1)"
        
        # Replace the 3 lines with new code
        $newLines = $newCode -split "`n"
        $lines = $lines[0..($startLine - 1)] + $newLines + $lines[($endLine + 1)..($lines.Length - 1)]
        
        $lines | Set-Content $filePath -Encoding UTF8
        Write-Host "✅ Replacement complete using line-based approach!"
    } else {
        Write-Host "❌ Could not find else block at expected location"
    }
}
