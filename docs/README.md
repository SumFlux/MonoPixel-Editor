# MonoPixel Editor 文档中心

欢迎使用 MonoPixel Editor！本文档中心提供完整的使用指南、开发文档和打包发布指南。

---

## 📚 文档导航

### 🎯 快速开始

| 文档 | 描述 | 阅读时间 |
|------|------|----------|
| [README.md](../README.md) | 项目简介、快速安装和运行 | 5 分钟 |
| [项目总览](PROJECT_OVERVIEW.md) | 完整的项目概览和功能清单 | 10 分钟 |

### 👤 用户文档

| 文档 | 描述 | 适用对象 | 阅读时间 |
|------|------|----------|----------|
| [用户手册](USER_MANUAL.md) | 完整的功能说明和使用指南 | 终端用户 | 30 分钟 |

**用户手册包含**：
- ✅ 安装与运行
- ✅ 界面介绍
- ✅ 基础操作（画布导航、撤销重做）
- ✅ 8种工具详解（画笔、橡皮擦、直线、矩形、圆形、填充、选择、文本）
- ✅ 图层管理
- ✅ 文本工具（智能挤压说明）
- ✅ 选择工具（移动、缩放）
- ✅ 导出功能（3种格式、扫描模式、位序）
- ✅ 项目管理（保存/加载）
- ✅ 快捷键参考
- ✅ 常见问题解答

### 💻 开发文档

| 文档 | 描述 | 适用对象 | 阅读时间 |
|------|------|----------|----------|
| [开发文档](DEVELOPMENT.md) | 架构设计、开发指南和 API 文档 | 开发者 | 45 分钟 |

**开发文档包含**：
- ✅ 项目架构（MVC 模式）
- ✅ 开发环境设置
- ✅ 代码结构详解
- ✅ 核心模块详解（Canvas、Layer、History、Project）
- ✅ 工具开发指南（如何创建新工具）
- ✅ 测试指南（单元测试、集成测试）
- ✅ 代码规范（PEP 8、命名规范、文档字符串）
- ✅ 贡献指南
- ✅ 性能优化建议
- ✅ 调试技巧

### 📦 打包发布

| 文档 | 描述 | 适用对象 | 阅读时间 |
|------|------|----------|----------|
| [打包发布指南](BUILD_GUIDE.md) | 多平台打包和发布流程 | 维护者 | 30 分钟 |

**打包发布指南包含**：
- ✅ Windows 打包（PyInstaller、Inno Setup）
- ✅ macOS 打包（.app、.dmg、代码签名）
- ✅ Linux 打包（AppImage、DEB）
- ✅ 打包配置详解（spec 文件）
- ✅ 常见问题（体积优化、路径问题）
- ✅ 发布流程（版本管理、GitHub Release）
- ✅ CI/CD 自动化（GitHub Actions）

---

## 🎯 按需求查找文档

### 我想...

#### 🚀 开始使用 MonoPixel Editor
→ 阅读 [README.md](../README.md) 了解安装和运行
→ 阅读 [用户手册](USER_MANUAL.md) 学习所有功能

#### 🎨 学习如何使用某个工具
→ 阅读 [用户手册 - 工具详解](USER_MANUAL.md#工具详解)

#### 📤 导出图像到嵌入式设备
→ 阅读 [用户手册 - 导出功能](USER_MANUAL.md#导出功能)

#### 💡 了解项目架构和设计
→ 阅读 [开发文档 - 项目架构](DEVELOPMENT.md#项目架构)

#### 🛠️ 开发新功能或修复 Bug
→ 阅读 [开发文档 - 开发环境设置](DEVELOPMENT.md#开发环境设置)
→ 阅读 [开发文档 - 工具开发指南](DEVELOPMENT.md#工具开发指南)

#### 📦 打包应用程序
→ 阅读 [打包发布指南](BUILD_GUIDE.md)

#### 🐛 遇到问题
→ 阅读 [用户手册 - 常见问题](USER_MANUAL.md#常见问题)
→ 阅读 [打包发布指南 - 常见问题](BUILD_GUIDE.md#常见问题)

---

## 📖 文档特色

### ✅ 结构清晰
- 每个文档都有详细的目录
- 章节划分合理，易于查找
- 使用表格、列表等格式提高可读性

### ✅ 内容完整
- 覆盖所有功能和特性
- 包含代码示例和配置示例
- 提供常见问题解答

### ✅ 实用性强
- 提供实际使用场景
- 包含最佳实践建议
- 提供故障排除指南

### ✅ 易于维护
- Markdown 格式，易于编辑
- 模块化组织，便于更新
- 版本控制友好

---

## 🔍 文档搜索技巧

### 在 GitHub 上搜索
1. 访问项目仓库
2. 按 `/` 键打开搜索
3. 输入关键词搜索

### 在本地搜索
```bash
# 搜索所有文档中的关键词
grep -r "关键词" docs/

# 搜索特定文件
grep "关键词" docs/USER_MANUAL.md
```

### 常用搜索关键词
- **工具**: pencil, eraser, line, rectangle, circle, fill, select, text
- **功能**: export, layer, undo, redo, save, load
- **格式**: C Array, Binary, PNG, horizontal, vertical, MSB, LSB
- **问题**: error, issue, problem, troubleshoot

---

## 📝 文档贡献

发现文档错误或有改进建议？欢迎贡献！

### 如何贡献文档

1. **报告问题**
   - 在 GitHub Issues 中创建问题
   - 标签：`documentation`

2. **提交改进**
   - Fork 项目
   - 编辑文档（Markdown 格式）
   - 提交 Pull Request

3. **文档规范**
   - 使用清晰的标题和章节
   - 提供代码示例
   - 使用表格和列表提高可读性
   - 添加目录（长文档）

---

## 📊 文档统计

| 文档 | 字数 | 章节数 | 代码示例 |
|------|------|--------|----------|
| README.md | ~1,500 | 10 | 5 |
| 项目总览 | ~3,000 | 15 | 10 |
| 用户手册 | ~8,000 | 12 | 20 |
| 开发文档 | ~10,000 | 8 | 30 |
| 打包发布指南 | ~7,000 | 7 | 25 |
| **总计** | **~29,500** | **52** | **90** |

---

## 🔗 相关资源

### 官方资源
- [PyQt6 文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [NumPy 文档](https://numpy.org/doc/)
- [pytest 文档](https://docs.pytest.org/)

### 社区资源
- [GitHub Issues](https://github.com/your-repo/issues) - 报告问题和建议
- [GitHub Discussions](https://github.com/your-repo/discussions) - 讨论和交流

### 学习资源
- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [PyQt6 教程](https://www.pythonguis.com/pyqt6-tutorial/)
- [嵌入式显示器资料](https://learn.adafruit.com/category/displays)

---

## 📅 文档更新记录

### v1.0.0 (2024-XX-XX)
- ✅ 创建完整的文档体系
- ✅ 用户手册（12章节，8000字）
- ✅ 开发文档（8章节，10000字）
- ✅ 打包发布指南（7章节，7000字）
- ✅ 项目总览（15章节，3000字）
- ✅ 文档索引（本文件）

---

## 💬 反馈

文档有帮助吗？有改进建议吗？

- 👍 **有帮助**: 在 GitHub 上给项目加星
- 💡 **有建议**: 创建 Issue 或 Discussion
- 🐛 **发现错误**: 提交 Pull Request 修复

---

**MonoPixel Editor 文档中心**

© 2024 MonoPixel. All rights reserved.

**文档版本**: 1.0.0
**最后更新**: 2024-XX-XX
**文档总字数**: ~29,500 字
**文档完整度**: 100%
