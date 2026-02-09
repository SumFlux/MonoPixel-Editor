@echo off
REM MonoPixel Editor Build Script

echo ========================================
echo MonoPixel Editor Build Tool
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not installed
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] PyInstaller installation failed
        pause
        exit /b 1
    )
)

echo [1/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] Building application...
pyinstaller MonoPixelEditor.spec

if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo [3/3] Build completed!
echo.
echo Executable location: dist\MonoPixelEditor.exe
echo.
pause
