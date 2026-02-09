# MonoPixel Editor 快速打包指南

> ⚡ 5 分钟快速打包 - 适合新手开发者

本指南提供最简化的打包步骤。如需详细说明，请参考 [完整打包指南](BUILD_GUIDE.md)。

---

## 📋 前置要求

- ✅ Python 3.10+ 已安装
- ✅ 项目依赖已安装（`pip install -r requirements.txt`）
- ✅ 应用程序可以正常运行（`cd src && python main.py`）

---

## 🚀 Windows 快速打包

### 方法 1: 使用打包脚本（推荐）

```bash
# 在项目根目录执行
build.bat
```

**就这么简单！** 脚本会自动：
1. 检查并安装 PyInstaller
2. 清理旧的构建文件
3. 执行打包
4. 生成可执行文件到 `dist/MonoPixelEditor.exe`

### 方法 2: 手动打包

```bash
# 1. 安装 PyInstaller（如果未安装）
pip install pyinstaller

# 2. 执行打包
pyinstaller MonoPixelEditor.spec

# 3. 测试可执行文件
dist\MonoPixelEditor.exe
```

---

## 🍎 macOS 快速打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 执行打包
pyinstaller MonoPixelEditor.spec

# 3. 测试应用
open dist/MonoPixelEditor.app
```

---

## 🐧 Linux 快速打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 执行打包
pyinstaller MonoPixelEditor.spec

# 3. 测试可执行文件
./dist/MonoPixelEditor
```

---

## ✅ 验证打包结果

打包完成后，请测试以下功能：

- [ ] 应用程序正常启动
- [ ] 界面样式正确显示（深色主题）
- [ ] 绘图工具正常工作
- [ ] 导出功能正常
- [ ] 保存/加载项目正常

---

## ❌ 常见问题快速修复

### 问题 1: 打包后应用无法启动

**解决方法**：
```bash
# 临时启用控制台查看错误信息
# 编辑 MonoPixelEditor.spec，修改：
console=True  # 改为 True

# 重新打包
pyinstaller MonoPixelEditor.spec
```

### 问题 2: 样式表未加载（界面是白色的）

**原因**：样式文件未包含在打包中

**解决方法**：
检查 `MonoPixelEditor.spec` 中的 `datas` 配置：
```python
datas=[
    ('src/ui/style.qss', 'src/ui'),  # 确保这一行存在
]
```

### 问题 3: 打包文件体积过大

**解决方法**：
```bash
# 1. 使用虚拟环境（只安装必要依赖）
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 2. 安装依赖
pip install -r requirements.txt

# 3. 重新打包
pyinstaller MonoPixelEditor.spec
```

### 问题 4: ModuleNotFoundError

**原因**：缺少隐式导入的模块

**解决方法**：
在 `MonoPixelEditor.spec` 的 `hiddenimports` 中添加缺失的模块：
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

---

## 📚 进阶指南

需要更多功能？查看以下文档：

| 需求 | 文档 |
|------|------|
| 详细的打包配置说明 | [完整打包指南](../BUILD_GUIDE.md) |
| 创建安装程序（Windows .exe 安装包） | [完整打包指南 - Windows 安装程序](../BUILD_GUIDE.md#创建安装程序可选) |
| 创建 DMG 安装包（macOS） | [完整打包指南 - macOS DMG](../BUILD_GUIDE.md#创建-dmg-安装包可选) |
| 创建 AppImage/DEB（Linux） | [完整打包指南 - Linux 打包](../BUILD_GUIDE.md#linux-打包) |
| 代码签名 | [完整打包指南 - 代码签名](../BUILD_GUIDE.md#代码签名可选) |
| CI/CD 自动化 | [完整打包指南 - 自动化打包](../BUILD_GUIDE.md#自动化打包cicd) |
| 打包前检查清单 | [打包检查清单](BUILD_CHECKLIST.md) |
| 错误排查 | [常见错误排查手册](BUILD_TROUBLESHOOTING.md) |
| 最佳实践 | [打包最佳实践](BUILD_BEST_PRACTICES.md) |

---

## 🎯 下一步

打包成功后：

1. **测试打包文件** - 在干净的系统上测试所有功能
2. **创建发布版本** - 参考 [版本发布工作流](RELEASE_WORKFLOW.md)
3. **分发应用** - 上传到 GitHub Releases 或其他平台

---

## 💡 提示

- 💾 **首次打包**：可能需要 5-10 分钟下载依赖
- 🔄 **后续打包**：通常只需 1-2 分钟
- 📦 **文件大小**：Windows 约 50-80MB，macOS/Linux 约 60-90MB
- 🧪 **测试环境**：建议在虚拟机或干净系统上测试打包文件

---

**快速打包指南 v1.0**

需要帮助？查看 [完整打包指南](../BUILD_GUIDE.md) 或 [常见问题](../BUILD_GUIDE.md#常见问题)
