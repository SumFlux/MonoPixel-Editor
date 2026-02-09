# MonoPixel Editor 打包常见错误排查手册

> 🔧 系统化的错误诊断和解决方案

本手册帮助你快速定位和解决打包过程中的常见问题。

---

## 📑 目录

1. [环境相关错误](#环境相关错误)
2. [依赖相关错误](#依赖相关错误)
3. [打包配置错误](#打包配置错误)
4. [运行时错误](#运行时错误)
5. [资源文件错误](#资源文件错误)
6. [平台特定错误](#平台特定错误)
7. [调试技巧](#调试技巧)

---

## 环境相关错误

### 错误 1: PyInstaller 未安装

**症状**：
```
'pyinstaller' is not recognized as an internal or external command
```

**原因**：PyInstaller 未安装或未在 PATH 中

**解决方案**：
```bash
# 安装 PyInstaller
pip install pyinstaller

# 验证安装
pyinstaller --version
```

---

### 错误 2: Python 版本不兼容

**症状**：
```
ERROR: This package requires Python 3.10 or later
```

**原因**：Python 版本过低

**解决方案**：
```bash
# 检查 Python 版本
python --version

# 升级 Python 到 3.10+
# 或使用 pyenv/conda 管理多版本
```

---

### 错误 3: 虚拟环境未激活

**症状**：
- 打包后文件体积过大（>200MB）
- 包含不需要的依赖

**原因**：在全局环境打包，包含了所有已安装的包

**解决方案**：
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

# 重新打包
pyinstaller MonoPixelEditor.spec
```

---

## 依赖相关错误

### 错误 4: ModuleNotFoundError

**症状**：
```
ModuleNotFoundError: No module named 'PyQt6'
ModuleNotFoundError: No module named 'numpy'
```

**原因**：缺少隐式导入的模块

**解决方案**：

**方法 1**：在 `MonoPixelEditor.spec` 中添加到 `hiddenimports`
```python
hiddenimports=[
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'numpy',
    'PIL',
    'missing_module_name',  # 添加缺失的模块
]
```

**方法 2**：使用 `--hidden-import` 参数
```bash
pyinstaller --hidden-import=missing_module_name MonoPixelEditor.spec
```

---

### 错误 5: ImportError: DLL load failed

**症状**（Windows）：
```
ImportError: DLL load failed while importing QtCore
```

**原因**：缺少 Visual C++ 运行库或 Qt 依赖

**解决方案**：

1. **安装 Visual C++ Redistributable**
   - 下载：https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 安装后重新打包

2. **检查 PyQt6 安装**
   ```bash
   pip uninstall PyQt6
   pip install PyQt6
   ```

---

### 错误 6: 依赖版本冲突

**症状**：
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**原因**：依赖包版本不兼容

**解决方案**：
```bash
# 清理环境
pip uninstall -y -r requirements.txt

# 重新安装
pip install -r requirements.txt

# 或使用 pip-tools 锁定版本
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

---

## 打包配置错误

### 错误 7: spec 文件路径错误

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'src/main.py'
```

**原因**：spec 文件中的路径不正确

**解决方案**：

检查 `MonoPixelEditor.spec` 中的路径：
```python
a = Analysis(
    ['src/main.py'],  # 确保路径正确
    # ...
)
```

使用绝对路径（如果需要）：
```python
import os
spec_root = os.path.abspath(SPECPATH)

a = Analysis(
    [os.path.join(spec_root, 'src', 'main.py')],
    # ...
)
```

---

### 错误 8: 数据文件未包含

**症状**：
- 样式表未加载（界面是白色的）
- 图标未显示
- 字体未加载

**原因**：数据文件未在 spec 文件中配置

**解决方案**：

在 `MonoPixelEditor.spec` 中添加数据文件：
```python
datas=[
    ('src/ui/style.qss', 'src/ui'),
    ('fonts', 'fonts'),
    ('icons', 'icons'),
]
```

验证数据文件是否包含：
```bash
# 打包后检查
# Windows
dir dist\MonoPixelEditor\_internal

# macOS/Linux
ls -la dist/MonoPixelEditor/_internal
```

---

### 错误 9: 图标文件不存在

**症状**：
```
WARNING: Icon file 'icon.ico' not found
```

**原因**：spec 文件中指定的图标文件不存在

**解决方案**：

**方法 1**：创建图标文件
```bash
# 将 PNG 转换为 ICO（Windows）
# 使用在线工具或 ImageMagick
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

**方法 2**：注释掉图标配置
```python
exe = EXE(
    # ...
    # icon='icon.ico',  # 注释掉
)
```

---

## 运行时错误

### 错误 10: 应用启动后立即崩溃

**症状**：
- 双击可执行文件后闪退
- 无错误信息

**原因**：可能是多种原因

**解决方案**：

**步骤 1**：启用控制台查看错误
```python
# 编辑 MonoPixelEditor.spec
exe = EXE(
    # ...
    console=True,  # 改为 True
)
```

**步骤 2**：重新打包并运行
```bash
pyinstaller MonoPixelEditor.spec
dist\MonoPixelEditor.exe
```

**步骤 3**：根据错误信息修复问题

---

### 错误 11: FileNotFoundError: style.qss

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'src/ui/style.qss'
```

**原因**：代码中使用了错误的路径访问资源文件

**解决方案**：

使用 `sys._MEIPASS` 获取资源路径：
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
with open(style_path, 'r', encoding='utf-8') as f:
    app.setStyleSheet(f.read())
```

---

### 错误 12: 样式表未生效

**症状**：
- 应用启动正常
- 但界面是白色的，没有深色主题

**原因**：样式表文件未加载或路径错误

**解决方案**：

**步骤 1**：检查样式文件是否包含
```python
# 在 MonoPixelEditor.spec 中
datas=[
    ('src/ui/style.qss', 'src/ui'),
]
```

**步骤 2**：检查代码中的加载逻辑
```python
# 确保使用 get_resource_path()
style_path = get_resource_path('src/ui/style.qss')
```

**步骤 3**：添加调试输出
```python
print(f"Loading style from: {style_path}")
print(f"File exists: {style_path.exists()}")
```

---

### 错误 13: 字体未加载

**症状**：
- 文本工具无法使用自定义字体
- 字体列表为空

**原因**：字体文件未包含或路径错误

**解决方案**：

**步骤 1**：包含字体文件夹
```python
datas=[
    ('fonts', 'fonts'),
]
```

**步骤 2**：使用正确的路径加载字体
```python
font_dir = get_resource_path('fonts')
for font_file in font_dir.glob('*.ttf'):
    QFontDatabase.addApplicationFont(str(font_file))
```

---

## 资源文件错误

### 错误 14: 资源文件路径在不同平台不一致

**症状**：
- Windows 上正常，macOS/Linux 上找不到文件
- 或反之

**原因**：路径分隔符不一致（`\` vs `/`）

**解决方案**：

使用 `pathlib.Path` 或 `os.path.join`：
```python
from pathlib import Path

# 推荐：使用 pathlib
resource_path = Path('src') / 'ui' / 'style.qss'

# 或使用 os.path.join
import os
resource_path = os.path.join('src', 'ui', 'style.qss')
```

---

### 错误 15: 打包后文件体积过大

**症状**：
- Windows 可执行文件 > 200MB
- 包含不需要的依赖

**原因**：包含了不必要的模块

**解决方案**：

**方法 1**：排除不需要的模块
```python
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    'tkinter',
    'test',
    'unittest',
]
```

**方法 2**：启用 UPX 压缩
```python
exe = EXE(
    # ...
    upx=True,
)
```

**方法 3**：使用虚拟环境
```bash
# 创建干净的虚拟环境
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pyinstaller MonoPixelEditor.spec
```

---

## 平台特定错误

### 错误 16: Windows Defender 误报（Windows）

**症状**：
- 打包后的 .exe 被 Windows Defender 删除
- 提示：Trojan:Win32/Wacatac

**原因**：PyInstaller 打包的程序可能被误报为病毒

**解决方案**：

**方法 1**：代码签名（推荐）
```bash
# 购买代码签名证书
# 使用 signtool 签名
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com MonoPixelEditor.exe
```

**方法 2**：提交白名单
- 访问：https://www.microsoft.com/en-us/wdsi/filesubmission
- 提交误报文件

**方法 3**：临时禁用 Windows Defender（不推荐）

---

### 错误 17: macOS Gatekeeper 阻止（macOS）

**症状**：
```
"MonoPixelEditor.app" cannot be opened because the developer cannot be verified
```

**原因**：应用未签名

**解决方案**：

**方法 1**：代码签名（推荐）
```bash
codesign --force --deep --sign "Developer ID Application: Your Name" MonoPixelEditor.app
```

**方法 2**：临时允许
```bash
xattr -cr MonoPixelEditor.app
```

**方法 3**：系统设置
- 系统偏好设置 → 安全性与隐私
- 点击"仍要打开"

---

### 错误 18: Linux 缺少依赖（Linux）

**症状**：
```
error while loading shared libraries: libxcb-xinerama.so.0
```

**原因**：系统缺少 Qt 依赖库

**解决方案**：

**Ubuntu/Debian**：
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

**Fedora/RHEL**：
```bash
sudo dnf install xcb-util-cursor
```

**Arch Linux**：
```bash
sudo pacman -S libxcb
```

---

## 调试技巧

### 技巧 1: 启用详细日志

```bash
# 打包时启用详细输出
pyinstaller --log-level=DEBUG MonoPixelEditor.spec
```

### 技巧 2: 使用 --debug 模式

```python
# 在 spec 文件中
exe = EXE(
    # ...
    debug=True,  # 启用调试模式
    console=True,  # 显示控制台
)
```

### 技巧 3: 检查打包内容

```bash
# Windows
pyi-archive_viewer dist\MonoPixelEditor.exe

# macOS/Linux
pyi-archive_viewer dist/MonoPixelEditor
```

### 技巧 4: 测试单个模块

```python
# 创建测试脚本 test_import.py
try:
    import PyQt6.QtCore
    print("PyQt6.QtCore: OK")
except Exception as e:
    print(f"PyQt6.QtCore: FAIL - {e}")

try:
    import numpy
    print("numpy: OK")
except Exception as e:
    print(f"numpy: FAIL - {e}")
```

### 技巧 5: 使用 --onedir 模式调试

```bash
# 使用 --onedir 模式（而非 --onefile）
# 可以查看所有打包的文件
pyinstaller --onedir src/main.py
```

---

## 错误分类索引

### 按错误类型

| 错误类型 | 错误编号 |
|---------|---------|
| 环境错误 | 1, 2, 3 |
| 依赖错误 | 4, 5, 6 |
| 配置错误 | 7, 8, 9 |
| 运行时错误 | 10, 11, 12, 13 |
| 资源文件错误 | 14, 15 |
| 平台特定错误 | 16, 17, 18 |

### 按严重程度

| 严重程度 | 错误编号 |
|---------|---------|
| 🔴 严重（无法打包） | 1, 2, 4, 7 |
| 🟡 中等（打包成功但无法运行） | 10, 11, 12, 13 |
| 🟢 轻微（功能受限） | 8, 9, 14 |
| ⚠️  警告（可忽略） | 15, 16, 17, 18 |

---

## 常见问题快速查找

| 症状 | 可能原因 | 错误编号 |
|------|---------|---------|
| 打包命令不存在 | PyInstaller 未安装 | 1 |
| 打包失败，提示 Python 版本 | Python 版本过低 | 2 |
| 文件体积过大 | 未使用虚拟环境 | 3, 15 |
| 应用无法启动 | 缺少模块 | 4, 10 |
| DLL 加载失败 | 缺少运行库 | 5 |
| 界面是白色的 | 样式表未加载 | 8, 12 |
| 找不到文件 | 路径错误 | 7, 11, 14 |
| 字体无法使用 | 字体文件未包含 | 13 |
| Windows Defender 删除 | 误报病毒 | 16 |
| macOS 无法打开 | Gatekeeper 阻止 | 17 |
| Linux 缺少库 | 系统依赖缺失 | 18 |

---

## 获取帮助

如果本手册无法解决你的问题：

1. **查看完整打包指南**：[BUILD_GUIDE.md](../BUILD_GUIDE.md)
2. **查看 PyInstaller 文档**：https://pyinstaller.org/
3. **搜索 GitHub Issues**：https://github.com/pyinstaller/pyinstaller/issues
4. **提问**：
   - Stack Overflow: 标签 `pyinstaller`
   - PyInstaller 论坛：https://github.com/pyinstaller/pyinstaller/discussions

---

## 贡献

发现新的错误和解决方案？欢迎贡献！

1. Fork 项目
2. 添加新的错误和解决方案
3. 提交 Pull Request

---

**打包常见错误排查手册 v1.0**

© 2024 MonoPixel. All rights reserved.
