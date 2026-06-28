@echo off
REM ============================================================
REM  GroceryPOS Pro — Windows Build Script
REM  Run from the project root directory:
REM      build_windows.bat
REM ============================================================

echo.
echo ============================================================
echo   GroceryPOS Pro - Building Windows EXE
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo [1/5] Installing / upgrading dependencies...
pip install --upgrade pip >nul 2>&1
pip install pyinstaller openpyxl reportlab python-barcode pillow >nul 2>&1
echo       Done.

echo.
echo [2/5] Running test suite...
python tests\test_pos_system.py
IF ERRORLEVEL 1 (
    echo [ERROR] Tests failed. Fix errors before building.
    pause
    exit /b 1
)

echo.
echo [3/5] Cleaning previous build...
if exist dist\GroceryPOS_Pro rmdir /s /q dist\GroceryPOS_Pro
if exist build\GroceryPOS_Pro rmdir /s /q build\GroceryPOS_Pro

echo.
echo [4/5] Building EXE with PyInstaller...
pyinstaller grocerypos.spec --clean --noconfirm
IF ERRORLEVEL 1 (
    echo [ERROR] PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo [5/5] Copying runtime folders to dist...
if not exist dist\GroceryPOS_Pro\data    mkdir dist\GroceryPOS_Pro\data
if not exist dist\GroceryPOS_Pro\logs    mkdir dist\GroceryPOS_Pro\logs
if not exist dist\GroceryPOS_Pro\backups mkdir dist\GroceryPOS_Pro\backups
if not exist dist\GroceryPOS_Pro\reports mkdir dist\GroceryPOS_Pro\reports
if not exist dist\GroceryPOS_Pro\assets  mkdir dist\GroceryPOS_Pro\assets

echo.
echo ============================================================
echo   BUILD COMPLETE
echo   Output: dist\GroceryPOS_Pro\GroceryPOS_Pro.exe
echo ============================================================
echo.
echo   To distribute: zip the entire dist\GroceryPOS_Pro\ folder.
echo.
pause
