# MonoPixel Editor 打包发布指南

> 📦 详细的多平台打包和发布流程

**相关文档**：
- [快速打包指南](packaging/QUICK_BUILD.md) - 5分钟快速开始
- [打包检查清单](packaging/BUILD_CHECKLIST.md) - 91项检查项
- [常见错误排查](packaging/BUILD_TROUBLESHOOTING.md) - 18种错误解决方案
- [打包最佳实践](packaging/BUILD_BEST_PRACTICES.md) - 经验和技巧
- [版本发布工作流](packaging/RELEASE_WORKFLOW.md) - 完整发布流程

---

## 目录

1. [打包准备](#打包准备)
2. [Windows 打包](#windows-打包)
3. [macOS 打包](#macos-打包)
4. [Linux 打包](#linux-打包)
5. [打包配置详解](#打包配置详解)
6. [常见问题](#常见问题)
7. [发布流程](#发布流程)

---

## 打包准备

### 1. 环境检查

确保已安装所有依赖：

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. 测试应用程序

在打包前，确保应用程序正常运行：

```bash
cd src
python main.py
```

测试清单：
- [ ] 应用程序正常启动
- [ ] 所有工具正常工作
- [ ] 导出功能正常
- [ ] 保存/加载项目正常
- [ ] 快捷键正常工作
- [ ] UI 样式正确显示

### 3. 运行单元测试

```bash
pytest tests/unit/ -v
```

确保所有测试通过。

### 4. 清理临时文件

```bash
# Windows
rmdir /s /q build dist __pycache__
del /q *.spec

# macOS/Linux
rm -rf build dist __pycache__
rm -f *.spec
```

---

## Windows 打包

### 方法 1: 使用打包脚本（推荐）

**步骤 1**: 运行打包脚本

```bash
build.bat
```

脚本会自动：
1. 检查 PyInstaller 是否安装
2. 清理旧的构建文件
3. 使用 `MonoPixelEditor.spec` 打包
4. 生成可执行文件到 `dist/` 目录

**步骤 2**: 测试可执行文件

```bash
dist\MonoPixelEditor.exe
```

### 方法 2: 手动打包

**步骤 1**: 生成 spec 文件（首次）

```bash
pyi-makespec --onefile --windowed --name=MonoPixelEditor src/main.py
```

**步骤 2**: 编辑 spec 文件

参考 [打包配置详解](#打包配置详解) 章节。

**步骤 3**: 执行打包

```bash
pyinstaller MonoPixelEditor.spec
```

**步骤 4**: 测试

```bash
dist\MonoPixelEditor.exe
```

### 添加应用图标

**步骤 1**: 准备图标文件

- 格式: `.ico`
- 推荐尺寸: 256x256
- 放置位置: 项目根目录

**步骤 2**: 修改 spec 文件

```python
exe = EXE(
    # ... 其他参数
    icon='icon.ico',  # 添加这一行
)
```

**步骤 3**: 重新打包

```bash
pyinstaller MonoPixelEditor.spec
```

### 创建安装程序（可选）

使用 **Inno Setup** 创建 Windows 安装程序。

**步骤 1**: 下载并安装 Inno Setup

下载地址: https://jrsoftware.org/isdl.php

**步骤 2**: 创建安装脚本 `installer.iss`

```ini
[Setup]
AppName=MonoPixel Editor
AppVersion=1.0
DefaultDirName={pf}\MonoPixelEditor
DefaultGroupName=MonoPixel Editor
OutputDir=installer
OutputBaseFilename=MonoPixelEditor-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\MonoPixelEditor.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\MonoPixel Editor"; Filename: "{app}\MonoPixelEditor.exe"
Name: "{commondesktop}\MonoPixel Editor"; Filename: "{app}\MonoPixelEditor.exe"

[Run]
Filename: "{app}\MonoPixelEditor.exe"; Description: "Launch MonoPixel Editor"; Flags: postinstall nowait skipifsilent
```

**步骤 3**: 编译安装程序

在 Inno Setup 中打开 `installer.iss` 并编译。

---

## macOS 打包

### 方法 1: 使用 PyInstaller

**步骤 1**: 创建 spec 文件

```bash
pyi-makespec --onefile --windowed --name=MonoPixelEditor src/main.py
```

**步骤 2**: 编辑 spec 文件

```python
# MonoPixelEditor.spec

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/ui/style.qss', 'src/ui'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='MonoPixelEditor.app',
    icon='icon.icns',  # macOS 图标
    bundle_identifier='com.monopixel.editor',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
    },
)
```

**步骤 3**: 执行打包

```bash
pyinstaller MonoPixelEditor.spec
```

**步骤 4**: 测试

```bash
open dist/MonoPixelEditor.app
```

### 创建 DMG 安装包（可选）

**步骤 1**: 安装 create-dmg

```bash
brew install create-dmg
```

**步骤 2**: 创建 DMG

```bash
create-dmg \
  --volname "MonoPixel Editor" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "MonoPixelEditor.app" 200 190 \
  --hide-extension "MonoPixelEditor.app" \
  --app-drop-link 600 185 \
  "MonoPixelEditor-1.0.dmg" \
  "dist/"
```

### 代码签名（可选）

```bash
codesign --force --deep --sign "Developer ID Application: Your Name" dist/MonoPixelEditor.app
```

---

## Linux 打包

### 方法 1: 使用 PyInstaller

**步骤 1**: 创建 spec 文件

```bash
pyi-makespec --onefile --windowed --name=MonoPixelEditor src/main.py
```

**步骤 2**: 编辑 spec 文件（同 Windows）

**步骤 3**: 执行打包

```bash
pyinstaller MonoPixelEditor.spec
```

**步骤 4**: 测试

```bash
./dist/MonoPixelEditor
```

### 方法 2: 创建 AppImage

**步骤 1**: 安装 appimagetool

```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

**步骤 2**: 创建 AppDir 结构

```bash
mkdir -p MonoPixelEditor.AppDir/usr/bin
mkdir -p MonoPixelEditor.AppDir/usr/share/applications
mkdir -p MonoPixelEditor.AppDir/usr/share/icons/hicolor/256x256/apps
```

**步骤 3**: 复制文件

```bash
cp dist/MonoPixelEditor MonoPixelEditor.AppDir/usr/bin/
cp icon.png MonoPixelEditor.AppDir/usr/share/icons/hicolor/256x256/apps/monopixeleditor.png
```

**步骤 4**: 创建 desktop 文件

```ini
# MonoPixelEditor.AppDir/usr/share/applications/monopixeleditor.desktop

[Desktop Entry]
Type=Application
Name=MonoPixel Editor
Exec=MonoPixelEditor
Icon=monopixeleditor
Categories=Graphics;
```

**步骤 5**: 创建 AppRun 脚本

```bash
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib/:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/MonoPixelEditor" "$@"
```

```bash
chmod +x MonoPixelEditor.AppDir/AppRun
```

**步骤 6**: 生成 AppImage

```bash
./appimagetool-x86_64.AppImage MonoPixelEditor.AppDir
```

### 方法 3: 创建 DEB 包

**步骤 1**: 安装 fpm

```bash
sudo apt-get install ruby ruby-dev rubygems build-essential
sudo gem install --no-document fpm
```

**步骤 2**: 创建包结构

```bash
mkdir -p package/usr/local/bin
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/256x256/apps

cp dist/MonoPixelEditor package/usr/local/bin/
cp monopixeleditor.desktop package/usr/share/applications/
cp icon.png package/usr/share/icons/hicolor/256x256/apps/monopixeleditor.png
```

**步骤 3**: 生成 DEB 包

```bash
fpm -s dir -t deb -n monopixeleditor -v 1.0 \
    --description "MonoPixel Editor - Pixel art editor for embedded displays" \
    --url "https://github.com/your-repo" \
    --license "MIT" \
    -C package \
    usr/local/bin usr/share
```

---

## 打包配置详解

### MonoPixelEditor.spec 文件

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],              # 入口文件
    pathex=[],                     # 额外的搜索路径
    binaries=[],                   # 二进制文件
    datas=[                        # 数据文件
        ('src/ui/style.qss', 'src/ui'),  # (源路径, 目标路径)
    ],
    hiddenimports=[                # 隐式导入
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy',
        'PIL',
    ],
    hookspath=[],                  # 自定义 hook 路径
    hooksconfig={},                # Hook 配置
    runtime_hooks=[],              # 运行时 hook
    excludes=[],                   # 排除的模块
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
    name='MonoPixelEditor',        # 可执行文件名
    debug=False,                   # 调试模式
    bootloader_ignore_signals=False,
    strip=False,                   # 去除符号表
    upx=True,                      # 使用 UPX 压缩
    upx_exclude=[],                # UPX 排除列表
    runtime_tmpdir=None,           # 运行时临时目录
    console=False,                 # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,        # 代码签名身份
    entitlements_file=None,        # macOS 权限文件
    icon='icon.ico',               # 应用图标
)
```

### 关键参数说明

**Analysis 参数**:

- `datas`: 包含非 Python 文件（如 QSS、图片、字体）
  ```python
  datas=[
      ('src/ui/style.qss', 'src/ui'),
      ('assets/fonts/*.ttf', 'assets/fonts'),
  ]
  ```

- `hiddenimports`: 动态导入的模块
  ```python
  hiddenimports=[
      'PyQt6.QtCore',
      'PyQt6.QtGui',
      'PyQt6.QtWidgets',
  ]
  ```

- `excludes`: 排除不需要的模块（减小体积）
  ```python
  excludes=[
      'matplotlib',
      'scipy',
      'pandas',
  ]
  ```

**EXE 参数**:

- `console=False`: GUI 应用不显示控制台
- `console=True`: 调试时显示控制台
- `upx=True`: 使用 UPX 压缩（减小体积 30-50%）
- `icon='icon.ico'`: 应用图标

### 包含额外文件

如果需要包含额外的文件（如字体、图片）：

```python
datas=[
    ('src/ui/style.qss', 'src/ui'),
    ('assets/fonts', 'assets/fonts'),
    ('assets/icons', 'assets/icons'),
]
```

在代码中访问这些文件：

```python
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """获取资源文件路径（支持打包后）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后
        return Path(sys._MEIPASS) / relative_path
    else:
        # 开发环境
        return Path(__file__).parent / relative_path

# 使用
style_path = get_resource_path('src/ui/style.qss')
```

---

## 常见问题

### Q1: 打包后应用无法启动

**可能原因**:
1. 缺少依赖模块
2. 缺少数据文件
3. 路径问题

**解决方法**:

1. **检查控制台输出**（设置 `console=True`）
   ```python
   exe = EXE(
       # ...
       console=True,  # 临时启用
   )
   ```

2. **添加缺失的模块到 hiddenimports**
   ```python
   hiddenimports=[
       'PyQt6.QtCore',
       'missing_module',  # 添加缺失的模块
   ]
   ```

3. **检查数据文件路径**
   ```python
   # 使用 get_resource_path() 函数
   style_path = get_resource_path('src/ui/style.qss')
   ```

### Q2: 打包后文件体积过大

**优化方法**:

1. **启用 UPX 压缩**
   ```python
   exe = EXE(
       # ...
       upx=True,
   )
   ```

2. **排除不需要的模块**
   ```python
   excludes=[
       'matplotlib',
       'scipy',
       'pandas',
       'tkinter',
   ]
   ```

3. **使用 --onefile 模式**
   ```bash
   pyinstaller --onefile src/main.py
   ```

4. **清理 Python 环境**
   - 使用虚拟环境
   - 只安装必要的依赖

### Q3: 样式表未加载

**原因**: 样式文件未包含在打包中

**解决方法**:

1. **添加到 datas**
   ```python
   datas=[
       ('src/ui/style.qss', 'src/ui'),
   ]
   ```

2. **使用正确的路径**
   ```python
   style_path = get_resource_path('src/ui/style.qss')
   with open(style_path, 'r', encoding='utf-8') as f:
       app.setStyleSheet(f.read())
   ```

### Q4: Windows Defender 误报

**原因**: PyInstaller 打包的程序可能被误报为病毒

**解决方法**:

1. **代码签名**（推荐）
   - 购买代码签名证书
   - 使用 `signtool` 签名

2. **提交白名单**
   - 向 Microsoft 提交误报
   - 网址: https://www.microsoft.com/en-us/wdsi/filesubmission

3. **使用其他打包工具**
   - cx_Freeze
   - py2exe

### Q5: macOS 无法打开应用

**原因**: macOS Gatekeeper 阻止未签名的应用

**解决方法**:

1. **代码签名**（推荐）
   ```bash
   codesign --force --deep --sign "Developer ID" MonoPixelEditor.app
   ```

2. **临时允许**
   ```bash
   xattr -cr MonoPixelEditor.app
   ```

3. **系统设置**
   - 系统偏好设置 → 安全性与隐私
   - 点击"仍要打开"

---

## 发布流程

### 1. 版本管理

**更新版本号**:

在以下文件中更新版本号：
- `src/main.py`
- `README.md`
- `MonoPixelEditor.spec`
- `installer.iss`（如果使用）

### 2. 创建 Git 标签

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 3. 打包所有平台

**Windows**:
```bash
build.bat
```

**macOS**:
```bash
pyinstaller MonoPixelEditor.spec
create-dmg ...
```

**Linux**:
```bash
pyinstaller MonoPixelEditor.spec
./appimagetool-x86_64.AppImage MonoPixelEditor.AppDir
```

### 4. 测试打包文件

在干净的系统上测试：
- [ ] 应用正常启动
- [ ] 所有功能正常
- [ ] 样式正确显示
- [ ] 导出功能正常

### 5. 创建 GitHub Release

1. 访问 GitHub 仓库
2. 点击 "Releases" → "Create a new release"
3. 选择标签（v1.0.0）
4. 填写发布说明
5. 上传打包文件：
   - `MonoPixelEditor-1.0-Windows.exe`
   - `MonoPixelEditor-1.0-macOS.dmg`
   - `MonoPixelEditor-1.0-Linux.AppImage`
6. 发布

### 6. 发布说明模板

```markdown
# MonoPixel Editor v1.0.0

## 新功能

- ✨ 完整的绘图工具集（7种工具）
- ✨ 智能文本渲染（半角挤压 45%-55%）
- ✨ 选择工具（移动、缩放）
- ✨ 多格式导出（C Array、Binary、PNG）

## 改进

- 🎨 深色主题 UI
- ⚡ 性能优化
- 📝 完善的文档

## Bug 修复

- 🐛 修复图层混合问题
- 🐛 修复导出预览错误

## 下载

- [Windows (64-bit)](link-to-windows-exe)
- [macOS (Intel/Apple Silicon)](link-to-dmg)
- [Linux (AppImage)](link-to-appimage)

## 系统要求

- Windows 7/10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

## 安装说明

详见 [用户手册](docs/USER_MANUAL.md)
```

---

## 自动化打包（CI/CD）

### GitHub Actions 示例

创建 `.github/workflows/build.yml`:

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
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: pyinstaller MonoPixelEditor.spec
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: MonoPixelEditor-Windows
          path: dist/MonoPixelEditor.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: pyinstaller MonoPixelEditor.spec
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: MonoPixelEditor-macOS
          path: dist/MonoPixelEditor.app

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: pyinstaller MonoPixelEditor.spec
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: MonoPixelEditor-Linux
          path: dist/MonoPixelEditor

  release:
    needs: [build-windows, build-macos, build-linux]
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v2
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

## 总结

### 打包清单

- [ ] 更新版本号
- [ ] 运行所有测试
- [ ] 清理临时文件
- [ ] 配置 spec 文件
- [ ] 添加应用图标
- [ ] 执行打包
- [ ] 测试可执行文件
- [ ] 创建安装程序（可选）
- [ ] 代码签名（可选）
- [ ] 创建 GitHub Release
- [ ] 更新文档

### 推荐工具

- **PyInstaller**: 跨平台打包
- **Inno Setup**: Windows 安装程序
- **create-dmg**: macOS DMG 创建
- **appimagetool**: Linux AppImage 创建
- **fpm**: 多格式包管理器

---

**MonoPixel Editor Build Team**
© 2024 MonoPixel. All rights reserved.
