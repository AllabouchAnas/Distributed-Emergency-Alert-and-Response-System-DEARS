$file = "app\client\alerts\templates\responder_dashboard_minimal.html"
$content = Get-Content $file -Raw -Encoding UTF8

# Fix all instances of the syntax error
$content = $content -replace "unit\.status=='ON_SCENE'", "unit.status == 'ON_SCENE'"
$content = $content -replace "unit\.status !='ON_SCENE'", "unit.status != 'ON_SCENE'"
$content = $content -replace "unit\.status!='ON_SCENE'", "unit.status != 'ON_SCENE'"
$content = $content -replace "unit\.status =='ON_SCENE'", "unit.status == 'ON_SCENE'"

# Also fix any potential split-line issues
$content = $content -replace "{% if unit\.status == 'ON_SCENE' %}disabled\{%\s+endif %}", "{% if unit.status == 'ON_SCENE' %}disabled{% endif %}"
$content = $content -replace "{% if unit\.status != 'ON_SCENE'\s+%}disabled", "{% if unit.status != 'ON_SCENE' %}disabled"

# Write back with UTF-8 encoding WITHOUT BOM
[System.IO.File]::WriteAllText((Resolve-Path $file).Path, $content, (New-Object System.Text.UTF8Encoding $false))

Write-Host "Fixed template syntax errors!" -ForegroundColor Green

# Verify the fix
$check = Get-Content $file -Raw -Encoding UTF8
if ($check -match "unit\.status=='ON_SCENE'" -or $check -match "unit\.status !='ON_SCENE'") {
    Write-Host "ERROR: Syntax errors still present!" -ForegroundColor Red
} else {
    Write-Host "VERIFIED: All syntax errors have been corrected!" -ForegroundColor Green
}
