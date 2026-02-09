# MonoPixel Editor 打包最佳实践

> 💡 经验总结和优化技巧

本文档总结了打包过程中的最佳实践，帮助你创建高质量的可执行文件。

---

## 📑 目录

1. [项目结构最佳实践](#项目结构最佳实践)
2. [依赖管理最佳实践](#依赖管理最佳实践)
3. [打包配置最佳实践](#打包配置最佳实践)
4. [体积优化技巧](#体积优化技巧)
5. [性能优化建议](#性能优化建议)
6. [安全性考虑](#安全性考虑)
7. [跨平台兼容性](#跨平台兼容性)
8. [持续集成最佳实践](#持续集成最佳实践)

---

## 项目结构最佳实践

### 1.1 推荐的目录结构

```
project/
├── src/                    # 源代码
│   ├── main.py            # 入口文件
│   ├── core/              # 核心模块
│   ├── ui/                # UI 模块
│   ├── services/          # 业务逻辑
│   └── utils/             # 工具函数
├── tests/                 # 测试代码
├── docs/                  # 文档
├── resources/             # 资源文件
│   ├── icons/            # 图标
│   ├── fonts/            # 字体
│   └── styles/           # 样式
├── build/                 # 构建临时文件（.gitignore）
├── dist/                  # 打包输出（.gitignore）
├── requirements.txt       # 依赖列表
├── MonoPixelEditor.spec  # PyInstaller 配置
├── build.bat             # Windows 打包脚本
├── build.sh              # macOS/Linux 打包脚本
└── README.md             # 项目说明
```

**优点**：
- ✅ 清晰的模块划分
- ✅ 资源文件集中管理
- ✅ 易于维护和扩展

---

### 1.2 资源文件组织

**推荐做法**：
```
resources/
├── icons/
│   ├── app.ico           # Windows 图标
│   ├── app.icns          # macOS 图标
│   └── app.png           # Linux 图标
├── fonts/
│   ├── README.md         # 字体说明
│   └── *.ttf             # 字体文件
└── styles/
    └── style.qss         # 样式表
```

**在代码中访问**：
```python
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """获取资源文件路径（支持打包后）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境
        base_path = Path(__file__).parent.parent

    return base_path / relative_path

# 使用
icon_path = get_resource_path('resources/icons/app.ico')
style_path = get_resource_path('resources/styles/style.qss')
```

---

### 1.3 配置文件管理

**推荐做法**：
```python
# config.py
import os
from pathlib import Path

class Config:
    # 应用信息
    APP_NAME = "MonoPixel Editor"
    APP_VERSION = "1.0.0"

    # 路径配置
    if hasattr(sys, '_MEIPASS'):
        BASE_DIR = Path(sys._MEIPASS)
    else:
        BASE_DIR = Path(__file__).parent

    RESOURCES_DIR = BASE_DIR / 'resources'
    ICONS_DIR = RESOURCES_DIR / 'icons'
    FONTS_DIR = RESOURCES_DIR / 'fonts'
    STYLES_DIR = RESOURCES_DIR / 'styles'

    # 用户数据目录
    USER_DATA_DIR = Path.home() / '.monopixel'
    USER_DATA_DIR.mkdir(exist_ok=True)
```

---

## 依赖管理最佳实践

### 2.1 使用虚拟环境

**推荐做法**：
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**优点**：
- ✅ 隔离项目依赖
- ✅ 减小打包体积
- ✅ 避免版本冲突

---

### 2.2 锁定依赖版本

**推荐做法**：

**requirements.txt**（开发环境）：
```
PyQt6>=6.6.0
numpy>=1.24.0
Pillow>=10.0.0
```

**requirements-lock.txt**（生产环境）：
```bash
# 生成锁定版本
pip freeze > requirements-lock.txt

# 使用锁定版本
pip install -r requirements-lock.txt
```

**或使用 pip-tools**：
```bash
# 安装 pip-tools
pip install pip-tools

# 创建 requirements.in
echo "PyQt6>=6.6.0" > requirements.in
echo "numpy>=1.24.0" >> requirements.in

# 生成锁定文件
pip-compile requirements.in

# 安装
pip-sync requirements.txt
```

---

### 2.3 最小化依赖

**推荐做法**：
- ✅ 只安装必要的包
- ✅ 避免安装开发工具（pytest, black, mypy）到生产环境
- ✅ 使用轻量级替代品

**示例**：
```
# ❌ 不推荐：安装完整的 scipy
scipy

# ✅ 推荐：只安装需要的子模块
scipy.ndimage
```

---

## 打包配置最佳实践

### 3.1 spec 文件模板

**推荐的 spec 文件结构**：
```python
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# 项目根目录
spec_root = Path(SPECPATH)

# 版本信息
VERSION = '1.0.0'

block_cipher = None

a = Analysis(
    # 入口文件
    [str(spec_root / 'src' / 'main.py')],

    # 额外的搜索路径
    pathex=[],

    # 二进制文件
    binaries=[],

    # 数据文件
    datas=[
        (str(spec_root / 'resources' / 'styles'), 'resources/styles'),
        (str(spec_root / 'resources' / 'icons'), 'resources/icons'),
        (str(spec_root / 'resources' / 'fonts'), 'resources/fonts'),
    ],

    # 隐式导入
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy',
        'PIL',
    ],

    # Hook 配置
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],

    # 排除的模块
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'tkinter',
        'test',
        'unittest',
    ],

    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MonoPixelEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(spec_root / 'resources' / 'icons' / 'app.ico'),
)

# macOS 特定配置
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='MonoPixelEditor.app',
        icon=str(spec_root / 'resources' / 'icons' / 'app.icns'),
        bundle_identifier='com.monopixel.editor',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': VERSION,
            'CFBundleVersion': VERSION,
        },
    )
```

---

### 3.2 打包脚本最佳实践

**Windows (build.bat)**：
```batch
@echo off
setlocal

echo ========================================
echo MonoPixel Editor Build Script
echo ========================================
echo.

REM 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found
    echo Please run: python -m venv .venv
    exit /b 1
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 检查 PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
)

REM 清理旧文件
echo [1/4] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 运行测试
echo [2/4] Running tests...
pytest tests/unit/ -v
if errorlevel 1 (
    echo [ERROR] Tests failed
    exit /b 1
)

REM 打包
echo [3/4] Building executable...
pyinstaller MonoPixelEditor.spec
if errorlevel 1 (
    echo [ERROR] Build failed
    exit /b 1
)

REM 验证
echo [4/4] Verifying build...
if not exist "dist\MonoPixelEditor.exe" (
    echo [ERROR] Executable not found
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Executable: dist\MonoPixelEditor.exe
echo ========================================
pause
```

---

## 体积优化技巧

### 4.1 启用 UPX 压缩

**推荐做法**：
```python
exe = EXE(
    # ...
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',  # 排除某些 DLL
    ],
)
```

**效果**：
- 减小 30-50% 体积
- 略微增加启动时间（可接受）

---

### 4.2 排除不需要的模块

**推荐做法**：
```python
excludes=[
    # 测试框架
    'pytest',
    'unittest',
    'test',

    # 科学计算（如果不需要）
    'matplotlib',
    'scipy',
    'pandas',

    # GUI 框架（如果不需要）
    'tkinter',
    'wx',

    # 其他
    'IPython',
    'jupyter',
]
```

---

### 4.3 使用 --onefile 模式

**推荐做法**：
```python
# 在 spec 文件中已经配置为 onefile
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # 包含所有文件
    a.zipfiles,
    a.datas,
    # ...
)
```

**优点**：
- ✅ 单个可执行文件
- ✅ 易于分发

**缺点**：
- ⚠️  启动时需要解压（略慢）
- ⚠️  体积可能略大

---

### 4.4 体积对比

| 优化方法 | 体积减少 | 启动时间影响 |
|---------|---------|-------------|
| 使用虚拟环境 | 50-70% | 无 |
| 启用 UPX 压缩 | 30-50% | +0.1-0.3s |
| 排除不需要的模块 | 20-40% | 无 |
| 使用 --onefile | -10% ~ +10% | +0.2-0.5s |

---

## 性能优化建议

### 5.1 延迟导入

**推荐做法**：
```python
# ❌ 不推荐：在模块顶部导入所有内容
import numpy as np
import PIL.Image
from PyQt6.QtWidgets import *

# ✅ 推荐：按需导入
def export_image():
    import numpy as np
    import PIL.Image
    # 使用 numpy 和 PIL
```

**优点**：
- ✅ 减少启动时间
- ✅ 减少内存占用

---

### 5.2 优化启动时间

**推荐做法**：

1. **延迟加载资源**：
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # 延迟加载字体
        QTimer.singleShot(0, self.load_fonts)

    def load_fonts(self):
        # 在主窗口显示后加载字体
        font_manager.load_fonts()
```

2. **使用启动画面**：
```python
# 显示启动画面
splash = QSplashScreen(QPixmap('splash.png'))
splash.show()
app.processEvents()

# 加载主窗口
window = MainWindow()

# 关闭启动画面
splash.finish(window)
window.show()
```

---

### 5.3 内存优化

**推荐做法**：

1. **及时释放资源**：
```python
def export_image(self):
    # 创建临时数组
    temp_data = np.zeros((height, width), dtype=bool)

    # 使用
    process_data(temp_data)

    # 显式删除
    del temp_data
```

2. **使用生成器**：
```python
# ❌ 不推荐：一次性加载所有数据
def get_all_pixels():
    return [pixel for pixel in canvas.data.flatten()]

# ✅ 推荐：使用生成器
def get_all_pixels():
    for pixel in canvas.data.flatten():
        yield pixel
```

---

## 安全性考虑

### 6.1 代码签名

**推荐做法**：

**Windows**：
```bash
# 使用 signtool 签名
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com MonoPixelEditor.exe
```

**macOS**：
```bash
# 代码签名
codesign --force --deep --sign "Developer ID Application: Your Name" MonoPixelEditor.app

# 公证（Notarization）
xcrun altool --notarize-app --file MonoPixelEditor.dmg --primary-bundle-id com.monopixel.editor
```

**优点**：
- ✅ 避免被杀毒软件误报
- ✅ 提高用户信任度
- ✅ macOS Gatekeeper 允许运行

---

### 6.2 不要包含敏感信息

**推荐做法**：

1. **使用环境变量**：
```python
# ❌ 不推荐：硬编码密钥
API_KEY = "sk-1234567890abcdef"

# ✅ 推荐：使用环境变量
API_KEY = os.getenv('API_KEY')
```

2. **使用配置文件**：
```python
# 从用户目录读取配置
config_path = Path.home() / '.monopixel' / 'config.json'
with open(config_path) as f:
    config = json.load(f)
```

---

### 6.3 校验和验证

**推荐做法**：

生成 SHA256 校验和：
```bash
# Windows
certutil -hashfile MonoPixelEditor.exe SHA256

# macOS/Linux
shasum -a 256 MonoPixelEditor
```

在发布说明中提供校验和：
```markdown
## 下载

- [Windows (64-bit)](link)
  - SHA256: `abc123...`
- [macOS (Intel/Apple Silicon)](link)
  - SHA256: `def456...`
```

---

## 跨平台兼容性

### 7.1 路径处理

**推荐做法**：
```python
from pathlib import Path

# ✅ 推荐：使用 pathlib
config_path = Path.home() / '.monopixel' / 'config.json'

# ❌ 不推荐：硬编码路径分隔符
config_path = os.path.expanduser('~/.monopixel/config.json')  # 在 Windows 上可能有问题
```

---

### 7.2 平台特定代码

**推荐做法**：
```python
import sys
import platform

if sys.platform == 'win32':
    # Windows 特定代码
    pass
elif sys.platform == 'darwin':
    # macOS 特定代码
    pass
elif sys.platform.startswith('linux'):
    # Linux 特定代码
    pass
```

---

### 7.3 字体处理

**推荐做法**：
```python
def get_default_font():
    """获取平台默认等宽字体"""
    if sys.platform == 'win32':
        return 'Consolas'
    elif sys.platform == 'darwin':
        return 'Menlo'
    else:  # Linux
        return 'DejaVu Sans Mono'
```

---

## 持续集成最佳实践

### 8.1 GitHub Actions 配置

**推荐做法**：

**.github/workflows/build.yml**：
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build
        run: pyinstaller MonoPixelEditor.spec

      - name: Test executable
        run: |
          dist\MonoPixelEditor.exe --version

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: MonoPixelEditor-Windows
          path: dist/MonoPixelEditor.exe

  # 类似的 macOS 和 Linux 任务
  # ...

  release:
    needs: [build-windows, build-macos, build-linux]
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            MonoPixelEditor-Windows/MonoPixelEditor.exe
            MonoPixelEditor-macOS/MonoPixelEditor.app
            MonoPixelEditor-Linux/MonoPixelEditor
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

### 8.2 自动化测试

**推荐做法**：
```yaml
- name: Run tests
  run: |
    pytest tests/unit/ -v --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

---

## 总结

### 关键要点

1. ✅ **使用虚拟环境** - 减小体积，避免冲突
2. ✅ **锁定依赖版本** - 确保可重现构建
3. ✅ **优化 spec 文件** - 正确配置资源和依赖
4. ✅ **启用 UPX 压缩** - 减小 30-50% 体积
5. ✅ **代码签名** - 避免误报，提高信任度
6. ✅ **跨平台测试** - 确保在所有平台正常工作
7. ✅ **自动化构建** - 使用 CI/CD 提高效率

### 检查清单

- [ ] 使用虚拟环境打包
- [ ] 锁定依赖版本
- [ ] 配置正确的 spec 文件
- [ ] 启用 UPX 压缩
- [ ] 排除不需要的模块
- [ ] 使用 get_resource_path() 访问资源
- [ ] 在所有平台测试
- [ ] 代码签名（生产环境）
- [ ] 生成 SHA256 校验和
- [ ] 设置 CI/CD 自动化

---

## 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [PyQt6 打包指南](https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-pyinstaller/)
- [代码签名指南](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)

---

**打包最佳实践 v1.0**

© 2024 MonoPixel. All rights reserved.
