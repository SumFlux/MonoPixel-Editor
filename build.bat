@echo off
REM MonoPixel Editor 打包脚本

echo ========================================
echo MonoPixel Editor 打包工具
echo ========================================
echo.

REM 检查 PyInstaller 是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未安装 PyInstaller
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)

echo [1/3] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] 开始打包应用程序...
pyinstaller MonoPixelEditor.spec

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [3/3] 打包完成！
echo.
echo 可执行文件位置: dist\MonoPixelEditor.exe
echo.
pause
