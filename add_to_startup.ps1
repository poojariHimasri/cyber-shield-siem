# Cyber Shield SIEM - Add to Windows Startup
# Run this script once to make the SIEM auto-start with Windows

$projectPath = "C:\Users\pooja\Desktop\cyber-shield-siem"
$runBatPath = "$projectPath\run.bat"
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\CyberShieldSIEM.lnk"

# Create a shortcut in Windows Startup folder
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $runBatPath
$shortcut.WorkingDirectory = $projectPath
$shortcut.Description = "Cyber Shield SIEM - Auto-starts the security monitoring dashboard"
$shortcut.WindowStyle = 7
$shortcut.Save()

Write-Host ""
Write-Host "=========================================="
Write-Host "  Cyber Shield SIEM added to Windows Startup!"
Write-Host "=========================================="
Write-Host "  It will auto-start every time you boot Windows"
Write-Host "  Dashboard: http://localhost:5000"
Write-Host "  Shortcut saved to Windows Startup folder"
Write-Host "=========================================="
Write-Host ""
Write-Host "To remove from startup, press Win + R, type 'shell:startup'"
Write-Host "and delete the 'CyberShieldSIEM.lnk' shortcut."
Write-Host ""
