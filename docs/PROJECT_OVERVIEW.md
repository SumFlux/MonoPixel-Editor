# MonoPixel Editor 项目总览

## 📋 项目信息

- **项目名称**: MonoPixel Editor
- **版本**: 1.0.0
- **开发语言**: Python 3.10+
- **GUI 框架**: PyQt6
- **许可证**: MIT License
- **开发状态**: ✅ 已完成（8/8 阶段 100%）

---

## 🎯 项目简介

MonoPixel Editor 是一个专为嵌入式 OLED/LCD 开发设计的单色像素画编辑器。它提供完整的绘图工具集、多图层管理、智能文本渲染和多种取模格式导出，是嵌入式开发者的理想工具。

### 核心特性

✅ **完整的绘图工具** (7种)
- 画笔工具（1-7px 笔触）
- 橡皮擦工具
- 直线工具（Shift 锁定角度）
- 矩形工具（3种填充模式）
- 圆形工具（3种填充模式）
- 油漆桶填充（泛洪算法）
- 选择工具（移动、缩放）

✅ **智能文本渲染**
- 半角字符智能挤压（45%-55%）
- 全角字符正常显示
- 系统字体 + 自定义字体支持

✅ **多图层系统**
- 透明混合
- 可见性/锁定控制
- 图层排序

✅ **撤销/重做**
- 50步历史记录
- 命令模式实现
- 所有操作可撤销

✅ **多格式导出**
- C Array（.h 文件）
- Binary（.bin 文件）
- PNG（.png 文件）
- 水平/垂直扫描
- MSB/LSB 位序
- 实时预览

✅ **项目管理**
- 保存/加载（.mpx 格式）
- 未保存提示
- JSON + Base64 编码

✅ **现代化 UI**
- 深色主题
- 完整快捷键系统
- 流畅交互体验

---

## 📁 项目结构

```
6_MonoPixel_Editor/
├── src/                          # 源代码
│   ├── main.py                   # 应用入口
│   ├── core/                     # 核心数据模型
│   │   ├── canvas.py             # 画布模型
│   │   ├── layer.py              # 图层模型
│   │   ├── history.py            # 历史记录（命令模式）
│   │   └── project.py            # 项目管理
│   ├── tools/                    # 绘图工具（8个工具）
│   │   ├── base_tool.py          # 工具基类
│   │   ├── pencil.py             # 画笔
│   │   ├── eraser.py             # 橡皮擦
│   │   ├── line.py               # 直线
│   │   ├── rectangle.py          # 矩形
│   │   ├── circle.py             # 圆形
│   │   ├── bucket_fill.py        # 填充
│   │   ├── select.py             # 选择工具
│   │   └── text.py               # 文本工具
│   ├── ui/                       # UI 视图层
│   │   ├── main_window.py        # 主窗口（含快捷键）
│   │   ├── canvas_view.py        # 画布视图
│   │   ├── toolbar.py            # 工具栏
│   │   ├── property_panel.py     # 属性面板
│   │   ├── layer_panel.py        # 图层面板
│   │   ├── export_di.py      # 导出对话框
│   │   └── style.qss             # 样式表（深色主题）
│   ├── services/                 # 业务逻辑服务
│   │   ├── export_service.py     # 导出服务（取模算法）
│   │   ├── text_service.py       # 文本渲染服务
│   │   ├── font_manager.py       # 字体管理
│   │   └── preview_service.py    # 预览服务
│   └── utils/                    # 工具函数
│       ├── bit_operations.py     # 位运算
│       ├── geometry.py           # 几何计算（Bresenham）
│       └── constants.py          # 常量定义
├── tests/                        # 测试代码
│   └── unit/                     # 单元测试（65+ 测试）
│       ├── test_canvas.py
│       ├── test_layer.py
│       ├── test_history.py
│       ├── test_export_service.py
│       ├── test_text_service.py
│       └── test_select_tool.py
├── docs/                         # 完整文档
│   ├── USER_MANUAL.md            # 用户手册（详细使用指南）
│   ├── DEVELOPMENT.md            # 开发文档（架构和 API）
│   ├── BUILD_GUIDE.md            # 打包发布指南
│   └── PROJECT_OVERVIEW.md       # 项目总览（本文件）
├── MonoPixelEditor.spec          # PyInstaller 配置
├── build.bat                     # 打包脚本（Windows）
├── requirements.txt              # 运行依赖
└── README.md                     # 项目说明
```

---

## 📖 文档导航

### 用户文档

| 文档 | 描述 | 适用对象 |
|------|------|----------|
| [README.md](../README.md) | 项目简介和快速开始 | 所有用户 |
| [用户手册](USER_MANUAL.md) | 完整的功能说明和使用指南 | 终端用户 |

**用户手册包含**：
- 安装与运行
- 界面介绍
- 基础操作（画布导航、撤销重做）
- 工具详解（8种工具的使用方法）
- 图层管理
- 文本工具（智能挤压说明）
- 选择工具（移动、缩放）
- 导出功能（3种格式、扫描模式、位序）
- 项目管理（保存/加载）
- 快捷键参考
- 常见问题

### 开发文档

| 文档 | 描述 | 适用对象 |
|------|------|----------|
| [开发文档](DEVELOPMENT.md) | 架构设计和开发指南 | 开发者 |
| [打包发布指南](BUILD_GUIDE.md) | 多平台打包流程 | 维护者 |

**开发文档包含**：
- 项目架构（MVC 模式）
- 开发环境设置
- 代码结构详解
- 核心模块详解（Canvas、Layer、History、Project）
- 工具开发指南（如何创建新工具）
- 测试指南（单元测试、集成测试）
- 代码规范（PEP 8、命名规范、文档字符串）
- 贡献指南

**打包发布指南包含**：
- Windows 打包（PyInstaller、Inno Setup）
- macOS 打包（.app、.dmg、代码签名）
- Linux 打包（AppImage、DEB）
- 打包配置详解（spec 文件）
- 常见问题（体积优化、路径问题）
- 发布流程（版本管理、GitHub Release）
- CI/CD 自动化（GitHub Actions）

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd 6_MonoPixel_Editor

# 安装依赖
pip install -r requirements.txt
```

### 运行

```bash
cd src
python main.py
```

### 打包

```bash
# Windows
build.bat

# macOS/Linux
pyinstaller MonoPixelEditor.spec
```

---

## 🎨 开发阶段

### Phase 1: 项目初始化与基础框架 ✅
- 创建项目目录结构
- 实现 Canvas 和 Layer 数据模型
- 实现 CanvasView（缩放、平移、网格线）
- 实现 MainWindow 主窗口布局
- 单元测试（12/12 通过）

### Phase 2: 基础绘图工具 ✅
- BaseTool 抽象基类
- 6种基础绘图工具
- 工具栏和属性面板 UI
- 实时预览功能
- 单元测试（22/22 通过）

### Phase 3: 图层系统 ✅
- 图层面板 UI
- 图层操作（可见性、锁定、重命名）
- 撤销/重做栈（命令模式）
- 绘图命令集成
- 单元测试（33/33 通过）

### Phase 4: 文本工具 ✅
- 字体管理器
- 文本渲染服务
- 半角字符智能挤压（45%-55%）
- 全角字符判断
- 文本工具实现

### Phase 5: 选择工具与缩放 ✅
- 选择工具（框选矩形区域）
- 选区移动（拖拽移动）
- 选区缩放（最近邻插值，8个手柄）
- 选区边框和手柄显示
- 撤销/重做支持

### Phase 6: 导出系统 ✅
- 位运算工具（MSB/LSB 打包解包）
- 水平扫描算法（逐行扫描）
- 垂直扫描算法（Page mode，OLED 专用）
- 导出为 C Array、Binary、PNG
- 导出对话框 UI
- 实时预览（反向解析验证）
- 单元测试（56/56 通过）

### Phase 7: 项目保存/加载 ✅
- 项目文件格式设计（JSON + Base64）
- 保存项目（.mpx 文件）
- 加载项目
- 修改标记（未保存提示）
- 新建画布功能
- 关闭时保存提示
- 单元测试（65/65 通过）

### Phase 8: UI 优化与打包 ✅
- 快捷键系统（文件、编辑、视图、工具切换）
- UI 样式优化（深色主题 QSS，370+ 行）
- PyInstaller 打包配置
- 打包脚本（build.bat）

---

## 🧪 测试

### 测试覆盖

- **单元测试**: 65+ 测试用例
- **测试覆盖率**: ≥ 80%
- **测试框架**: pytest + pytest-qt

### 运行测试

```bash
# 运行所有单元测试
pytest tests/unit/ -v

# 运行测试覆盖率
pytest tests/ --cov=src --cov-report=html
```

### 测试模块

- `test_canvas.py` - 画布模型测试
- `test_layer.py` - 图层模型测试
- `test_history.py` - 历史记录测试
- `test_export_service.py` - 导出服务测试
- `test_text_service.py` - 文本渲染测试
- `test_select_tool.py` - 选择工具测试
- 更多...

---

## 🛠️ 技术栈

### 核心技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 开发语言 |
| PyQt6 | 6.6.0+ | GUI 框架 |
| NumPy | 1.24.0+ | 数组处理、位运算 |
| Pillow | 10.0.0+ | 图像处理 |
| pytest | 7.4.0+ | 测试框架 |
| PyInstaller | 5.0+ | 打包工具 |

### 设计模式

- **MVC 模式**: 分离数据、视图和控制逻辑
- **命令模式**: 撤销/重做系统
- **策略模式**: 工具系统
- **观察者模式**: UI 更新（PyQt6 信号/槽）

### 核心算法

- **Bresenham 算法**: 直线和圆形绘制
- **泛洪填充**: 4-连通区域填充
- **最近邻插值**: 选区缩放
- **位运算**: MSB/LSB 打包解包
- **Base64 编码**: 项目文件存储

---

## 📊 项目统计

### 代码量

- **总代码行数**: ~8000+ 行
- **核心模块**: 4 个（core, tools, ui, services）
- **工具数量**: 8 种（7种绘图工具 + 1种选择工具）
- **UI 组件**: 6 个主要组件
- **测试用例**: 65+ 个

### 文件统计

- **Python 文件**: 30+ 个
- **测试文件**: 10+ 个
- **文档文件**: 5 个（完整文档）
- **配置文件**: 3 个

---

## ⌨️ 快捷键速查

### 文件操作
- `Ctrl+N` - 新建画布
- `Ctrl+O` - 打开项目
- `Ctrl+S` - 保存项目
- `Ctrl+E` - 导出

### 编辑操作
- `Ctrl+Z` - 撤销
- `Ctrl+Y` - 重做

### 视图操作
- `G` - 切换网格线
- `Ctrl+0` - 重置缩放
- `Ctrl+F` - 适应窗口
- `Ctrl++` / `Ctrl+-` - 放大/缩小

### 工具切换
- `1` - 画笔工具
- `2` - 橡皮擦工具
- `3` - 直线工具
- `4` - 矩形工具
- `5` - 圆形工具
- `6` - 油漆桶填充
- `7` - 选择工具
- `8` - 文本工具

---

## 🎯 使用场景

### 嵌入式开发

**OLED 显示器**（如 SSD1306）:
1. 创建 128x64 画布
2. 绘制图标或界面
3. 导出为 C Array（垂直扫描、MSB First）
4. 在 Arduino/STM32 中使用

**LCD 显示器**（如 Nokia 5110）:
1. 创建 84x48 画布
2. 绘制图形
3. 导出为 C Array（水平扫描、MSB First）
4. 在嵌入式项目中使用

### 像素艺术创作

1. 创建任意尺寸画布
2. 使用完整工具集创作
3. 多图层管理复杂作品
4. 导出为 PNG 分享

### 字体设计

1. 使用文本工具预览字体效果
2. 手动调整像素
3. 导出为位图字体
4. 用于嵌入式显示

---

## 🔧 扩展性

### 添加新工具

1. 继承 `BaseTool` 类
2. 实现 `on_press`, `on_drag`, `on_release` 方法
3. 注册到工具栏
4. 编写单元测试

详见 [开发文档 - 工具开发指南](DEVELOPMENT.md#工具开发指南)

### 添加新导出格式

1. 在 `ExportService` 中添加导出方法
2. 在 `ExportDialog` 中添加格式选项
3. 编写单元测试
4. 更新用户手册

### 自定义 UI 样式

1. 编辑 `src/ui/style.qss`
2. 使用 QSS 语法自定义样式
3. 重启应用查看效果

---

## 🐛 已知问题

### Windows

- ✅ 无已知问题

### macOS

- ⚠️ 未签名应用需要手动允许（Gatekeeper）
- 解决方法：`xattr -cr MonoPixelEditor.app`

### Linux

- ⚠️ 部分发行版可能缺少 Qt 依赖
- 解决方法：`sudo apt-get install libxcb-xinerama0`

---

## 📝 更新日志

### v1.0.0 (2024-XX-XX)

**新功能**:
- ✨ 完整的绘图工具集（8种工具）
- ✨ 智能文本渲染（半角挤压 45%-55%）
- ✨ 选择工具（移动、缩放）
- ✨ 多格式导出（C Array、Binary、PNG）
- ✨ 多图层系统
- ✨ 撤销/重做（50步）
- ✨ 项目保存/加载
- ✨ 深色主题 UI
- ✨ 完整快捷键系统

**技术特性**:
- 🏗️ MVC 架构
- 🎨 命令模式（撤销/重做）
- 🧪 65+ 单元测试
- 📦 PyInstaller 打包支持
- 📚 完整文档（用户手册、开发文档、打包指南）

---

## 🤝 贡献

欢迎贡献代码、报告 Bug 或提出建议！

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

详见 [开发文档 - 贡献指南](DEVELOPMENT.md#贡献指南)

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](../LICENSE) 文件。

---

## 📧 联系方式

- **GitHub Issues**: <repository-url>/issues
- **Email**: <your-email>
- **文档**: [docs/](.)

---

## 🙏 致谢

感谢以下开源项目：

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - 强大的 Python GUI 框架
- [NumPy](https://numpy.org/) - 高性能数组处理库
- [Pillow](https://python-pillow.org/) - Python 图像处理库
- [pytest](https://pytest.org/) - 优秀的测试框架
- [PyInstaller](https://www.pyinstaller.org/) - Python 打包工具

---

**MonoPixel Editor v1.0.0**

© 2024 MonoPixel. All rights reserved.

**项目状态**: ✅ 已完成（8/8 阶段 100%）

**最后更新**: 2024-XX-XX
