# MonoPixel Editor 打包检查清单

> 📋 确保打包质量的完整检查清单

使用本清单确保打包过程顺利，避免常见错误。

---

## 📌 使用说明

- ✅ 已完成
- ⏳ 进行中
- ❌ 未完成
- ⚠️  需要注意

---

## 阶段 1: 打包前准备

### 1.1 环境检查

- [ ] Python 版本正确（3.10+）
  ```bash
  python --version
  ```

- [ ] 所有依赖已安装
  ```bash
  pip list
  # 检查: PyQt6, numpy, Pillow, pyinstaller
  ```

- [ ] 虚拟环境已激活（推荐）
  ```bash
  # Windows
  .venv\Scripts\activate

  # macOS/Linux
  source .venv/bin/activate
  ```

### 1.2 代码质量检查

- [ ] 所有单元测试通过
  ```bash
  pytest tests/unit/ -v
  ```

- [ ] 应用程序正常运行
  ```bash
  cd src
  python main.py
  ```

- [ ] 无 console.log 或调试代码
  ```bash
  grep -r "print(" src/
  grep -r "console.log" src/
  ```

- [ ] 代码已提交到 Git
  ```bash
  git status
  # 应该显示: nothing to commit, working tree clean
  ```

### 1.3 版本管理

- [ ] 更新版本号
  - [ ] `src/main.py` 中的 `__version__`
  - [ ] `README.md` 中的版本号
  - [ ] `docs/PROJECT_OVERVIEW.md` 中的版本号

- [ ] 更新 CHANGELOG（如果有）
  - [ ] 新功能列表
  - [ ] Bug 修复列表
  - [ ] 已知问题

### 1.4 资源文件检查

- [ ] 样式文件存在
  - [ ] `src/ui/style.qss` 存在且正确

- [ ] 图标文件（如果使用）
  - [ ] `icon.ico` 存在（Windows）
  - [ ] `icon.icns` 存在（macOS）
  - [ ] `icon.png` 存在（Linux）

- [ ] 字体文件（如果使用）
  - [ ] `fonts/` 文件夹存在
  - [ ] 字体文件可访问

---

## 阶段 2: 打包配置检查

### 2.1 spec 文件检查

- [ ] `MonoPixelEditor.spec` 存在

- [ ] 入口文件路径正确
  ```python
  ['src/main.py']  # 检查路径
  ```

- [ ] 数据文件配置正确
  ```python
  datas=[
      ('src/ui/style.qss', 'src/ui'),
      # 其他资源文件
  ]
  ```

- [ ] 隐式导入配置完整
  ```python
  hiddenimports=[
      'PyQt6.QtCore',
      'PyQt6.QtGui',
      'PyQt6.QtWidgets',
      'numpy',
      'PIL',
  ]
  ```

- [ ] 图标路径正确（如果使用）
  ```python
  icon='icon.ico'  # 检查文件是否存在
  ```

- [ ] 控制台模式设置正确
  ```python
  console=False  # GUI 应用应该为 False
  ```

### 2.2 打包脚本检查

- [ ] `build.bat` 存在（Windows）
- [ ] 脚本有执行权限（macOS/Linux）
  ```bash
  chmod +x build.sh
  ```

---

## 阶段 3: 执行打包

### 3.1 清理旧文件

- [ ] 删除旧的构建文件
  ```bash
  # Windows
  rmdir /s /q build dist

  # macOS/Linux
  rm -rf build dist
  ```

### 3.2 执行打包

- [ ] 运行打包命令
  ```bash
  # 使用脚本
  build.bat  # Windows
  ./build.sh  # macOS/Linux

  # 或手动
  pyinstaller MonoPixelEditor.spec
  ```

- [ ] 打包过程无错误
  - [ ] 无 WARNING（或已知可忽略）
  - [ ] 无 ERROR

- [ ] 可执行文件已生成
  - [ ] Windows: `dist/MonoPixelEditor.exe`
  - [ ] macOS: `dist/MonoPixelEditor.app`
  - [ ] Linux: `dist/MonoPixelEditor`

---

## 阶段 4: 打包后测试

### 4.1 基础功能测试

- [ ] 应用程序正常启动
- [ ] 主窗口正确显示
- [ ] 界面样式正确（深色主题）
- [ ] 菜单栏正常工作
- [ ] 工具栏正常工作

### 4.2 核心功能测试

- [ ] **绘图工具**
  - [ ] 画笔工具
  - [ ] 橡皮擦工具
  - [ ] 直线工具
  - [ ] 矩形工具
  - [ ] 圆形工具
  - [ ] 油漆桶填充
  - [ ] 选择工具
  - [ ] 文本工具

- [ ] **图层系统**
  - [ ] 新建图层
  - [ ] 删除图层
  - [ ] 图层可见性切换
  - [ ] 图层顺序调整

- [ ] **撤销/重做**
  - [ ] Ctrl+Z 撤销
  - [ ] Ctrl+Y 重做
  - [ ] 多步撤销/重做

- [ ] **导出功能**
  - [ ] 导出为 C Array
  - [ ] 导出为 Binary
  - [ ] 导出为 PNG
  - [ ] 导出预览正确

- [ ] **项目管理**
  - [ ] 新建项目
  - [ ] 保存项目（.mpx）
  - [ ] 加载项目
  - [ ] 未保存提示

### 4.3 快捷键测试

- [ ] Ctrl+N - 新建画布
- [ ] Ctrl+S - 保存项目
- [ ] Ctrl+E - 导出
- [ ] Ctrl+Z - 撤销
- [ ] Ctrl+Y - 重做
- [ ] G - 切换网格线
- [ ] 1-8 - 工具切换

### 4.4 性能测试

- [ ] 启动时间 < 5 秒
- [ ] 绘图响应流畅
- [ ] 缩放/平移流畅
- [ ] 内存占用合理（< 200MB）

### 4.5 兼容性测试

- [ ] 在干净系统上测试（无 Python 环境）
- [ ] 在不同 Windows 版本测试（如适用）
  - [ ] Windows 10
  - [ ] Windows 11
- [ ] 在不同 macOS 版本测试（如适用）
- [ ] 在不同 Linux 发行版测试（如适用）

---

## 阶段 5: 文件大小和优化

### 5.1 文件大小检查

- [ ] 检查可执行文件大小
  ```bash
  # Windows
  dir dist\MonoPixelEditor.exe

  # macOS/Linux
  ls -lh dist/MonoPixelEditor
  ```

- [ ] 文件大小合理
  - [ ] Windows: 50-100MB
  - [ ] macOS: 60-120MB
  - [ ] Linux: 60-100MB

### 5.2 优化（如果需要）

- [ ] 启用 UPX 压缩
  ```python
  upx=True  # 在 spec 文件中
  ```

- [ ] 排除不需要的模块
  ```python
  excludes=[
      'matplotlib',
      'scipy',
      'pandas',
  ]
  ```

- [ ] 使用虚拟环境（只安装必要依赖）

---

## 阶段 6: 发布准备

### 6.1 文档检查

- [ ] README.md 更新
- [ ] 用户手册更新
- [ ] 打包指南更新
- [ ] CHANGELOG 更新（如果有）

### 6.2 Git 标签

- [ ] 创建版本标签
  ```bash
  git tag -a v1.0.0 -m "Release version 1.0.0"
  git push origin v1.0.0
  ```

### 6.3 发布文件准备

- [ ] 重命名可执行文件（包含版本号）
  - [ ] `MonoPixelEditor-1.0.0-Windows.exe`
  - [ ] `MonoPixelEditor-1.0.0-macOS.dmg`
  - [ ] `MonoPixelEditor-1.0.0-Linux.AppImage`

- [ ] 创建 SHA256 校验和
  ```bash
  # Windows
  certutil -hashfile MonoPixelEditor.exe SHA256

  # macOS/Linux
  shasum -a 256 MonoPixelEditor
  ```

### 6.4 发布说明

- [ ] 编写发布说明
  - [ ] 新功能列表
  - [ ] Bug 修复列表
  - [ ] 已知问题
  - [ ] 系统要求
  - [ ] 安装说明

---

## 阶段 7: 发布

### 7.1 GitHub Release

- [ ] 创建 GitHub Release
- [ ] 上传可执行文件
- [ ] 添加发布说明
- [ ] 添加 SHA256 校验和

### 7.2 发布后验证

- [ ] 下载链接可用
- [ ] 文件完整性验证
- [ ] 下载后可正常运行

---

## 📊 检查清单统计

| 阶段 | 检查项数量 | 完成数量 | 完成率 |
|------|-----------|---------|--------|
| 阶段 1: 打包前准备 | 15 | - | - |
| 阶段 2: 打包配置检查 | 12 | - | - |
| 阶段 3: 执行打包 | 6 | - | - |
| 阶段 4: 打包后测试 | 35 | - | - |
| 阶段 5: 文件大小和优化 | 8 | - | - |
| 阶段 6: 发布准备 | 10 | - | - |
| 阶段 7: 发布 | 5 | - | - |
| **总计** | **91** | **-** | **-%** |

---

## 🎯 关键检查点

以下是最关键的检查项，必须通过：

1. ✅ 所有单元测试通过
2. ✅ 应用程序正常运行（开发环境）
3. ✅ 打包过程无错误
4. ✅ 可执行文件已生成
5. ✅ 应用程序正常启动（打包后）
6. ✅ 核心功能正常工作（打包后）
7. ✅ 在干净系统上测试通过

---

## 💡 提示

- 📋 **打印清单**：可以打印本清单，逐项勾选
- 🔄 **重复使用**：每次打包都使用本清单
- 📝 **记录问题**：在清单上记录遇到的问题
- 🚀 **持续改进**：根据经验更新清单

---

## 📚 相关文档

- [快速打包指南](QUICK_BUILD.md) - 5 分钟快速打包
- [完整打包指南](../BUILD_GUIDE.md) - 详细的打包说明
- [常见错误排查](BUILD_TROUBLESHOOTING.md) - 错误解决方案
- [打包最佳实践](BUILD_BEST_PRACTICES.md) - 经验和技巧
- [版本发布工作流](RELEASE_WORKFLOW.md) - 完整发布流程

---

**打包检查清单 v1.0**

© 2024 MonoPixel. All rights reserved.
