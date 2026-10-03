@echo off
chcp 65001 >nul 2>&1
setlocal

set "DIR=%~dp0"
set "GSUDO=%DIR%gsudo64.exe"

echo ========================================
echo  JMS56x BOT Driver Uninstall
echo ========================================
echo.

if not exist "%GSUDO%" ( echo [ERROR] Missing: %GSUDO% & goto FAIL )

echo [1/2] Removing driver package from DriverStore...
"%GSUDO%" -d -- powershell -NoProfile -ExecutionPolicy Bypass -File "%DIR%remove-driver.ps1"

echo.
echo [2/2] Removing certificate from Trusted Root...
"%GSUDO%" -d -- powershell -NoProfile -Command "Remove-Item -Path 'Cert:\LocalMachine\Root\FA19D062DA35A7C752E6C2B046C37121624EAD9D' -ErrorAction SilentlyContinue; if (-not (Test-Path 'Cert:\LocalMachine\Root\FA19D062DA35A7C752E6C2B046C37121624EAD9D')) { Write-Host 'Certificate removed OK' } else { Write-Host 'Certificate still present' }"

echo.
echo ========================================
echo  Done! Unplug and replug the device.
echo  System will restore UAS driver.
echo ========================================
echo.
pause
exit /b 0

:FAIL
echo.
echo Uninstall aborted.
pause
exit /b 1