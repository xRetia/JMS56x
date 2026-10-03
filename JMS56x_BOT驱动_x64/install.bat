@echo off
chcp 65001 >nul 2>&1
setlocal

set "DIR=%~dp0"
set "GSUDO=%DIR%gsudo64.exe"
set "INF=%DIR%jms56xbot.inf"
set "CAT=%DIR%jms56xbot.cat"
set "CER=%DIR%JMS561TestSigner.cer"

echo ========================================
echo  JMS56x UAS to BOT Driver Install
echo ========================================
echo.

if not exist "%INF%"  ( echo [ERROR] Missing: %INF%  & goto FAIL )
if not exist "%CAT%"  ( echo [ERROR] Missing: %CAT%  & goto FAIL )
if not exist "%CER%"  ( echo [ERROR] Missing: %CER%  & goto FAIL )
if not exist "%GSUDO%" ( echo [ERROR] Missing: %GSUDO% & goto FAIL )

echo [1/2] Installing signing certificate to Trusted Root...
"%GSUDO%" -d -- powershell -NoProfile -Command "Import-Certificate -FilePath '%CER%' -CertStoreLocation Cert:\LocalMachine\Root -ErrorAction Stop | Out-Null; Write-Host 'Certificate installed OK'"
if errorlevel 1 (
    echo [ERROR] Certificate install failed.
    goto FAIL
)

echo.
echo [2/2] Adding driver package to DriverStore...
"%GSUDO%" -d -- powershell -NoProfile -Command "pnputil /add-driver '%INF%' /install"
if errorlevel 1 (
    echo [WARNING] pnputil returned non-zero, check output above.
)

echo.
echo ========================================
echo  Done! Unplug and replug the device.
echo  Device Manager should show:
echo  JMicron JMS56x USB 3.0 to SATA Adapter (BOT Mode)
echo ========================================
echo.
pause
exit /b 0

:FAIL
echo.
echo Install aborted.
pause
exit /b 1