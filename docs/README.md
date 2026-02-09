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
| [打包发布指南](BUILD_GUIDE.md) | 详细的多平台打包流程（主文档） | 所有开发者 | 30 分钟 |
| [快速打包指南](packaging/QUICK_BUILD.md) | 5分钟快速打包 | 新手开发者 | 5 分钟 |
| [打包检查清单](packaging/BUILD_CHECKLIST.md) | 完整的打包检查清单 | 所有开发者 | 10 分钟 |
| [常见错误排查](packaging/BUILD_TROUBLESHOOTING.md) | 系统化的错误诊断和解决 | 遇到问题的开发者 | 20 分钟 |
| [打包最佳实践](packaging/BUILD_BEST_PRACTICES.md) | 经验总结和优化技巧 | 有经验的开发者 | 25 分钟 |
| [版本发布工作流](packaging/RELEASE_WORKFLOW.md) | 完整的版本发布流程 | 项目维护者 | 20 分钟 |

**打包文档体系包含**：
- ✅ **快速开始**：5分钟快速打包（QUICK_BUILD.md）
- ✅ **详细指南**：Windows/macOS/Linux 完整流程（BUILD_GUIDE.md）
- ✅ **检查清单**：91项打包检查项（BUILD_CHECKLIST.md）
- ✅ **错误排查**：18种常见错误和解决方案（BUILD_TROUBLESHOOTING.md）
- ✅ **最佳实践**：项目结构、依赖管理、体积优化、安全性（BUILD_BEST_PRACTICES.md）
- ✅ **发布流程**：版本管理、打包测试、GitHub Release（RELEASE_WORKFLOW.md）

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
→ **新手**：阅读 [快速打包指南](packaging/QUICK_BUILD.md)（5分钟）
→ **详细流程**：阅读 [打包发布指南](BUILD_GUIDE.md)
→ **检查清单**：使用 [打包检查清单](packaging/BUILD_CHECKLIST.md)
→ **遇到问题**：查看 [常见错误排查](packaging/BUILD_TROUBLESHOOTING.md)

#### 🐛 遇到问题
→ **使用问题**：阅读 [用户手册 - 常见问题](USER_MANUAL.md#常见问题)
→ **打包问题**：阅读 [常见错误排查手册](packaging/BUILD_TROUBLESHOOTING.md)
→ **详细说明**：阅读 [打包发布指南 - 常见问题](BUILD_GUIDE.md#常见问题)

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
- **打包**: build, package, pyinstaller, spec, dist
- **问题**: error, issue, problem, troubleshoot, fix

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
| 快速打包指南 | ~1,500 | 6 | 10 |
| 打包检查清单 | ~3,000 | 7 | 5 |
| 常见错误排查 | ~5,000 | 7 | 30 |
| 打包最佳实践 | ~6,000 | 8 | 40 |
| 版本发布工作流 | ~4,000 | 6 | 20 |
| **总计** | **~49,000** | **86** | **195** |

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

### v1.0.0 (2026-02-09)
- ✅ 创建完整的文档体系
- ✅ 用户手册（12章节，8000字）
- ✅ 开发文档（8章节，10000字）
- ✅ 打包发布指南（7章节，7000字）
- ✅ 快速打包指南（6章节，1500字）
- ✅ 打包检查清单（7章节，3000字）
- ✅ 常见错误排查（7章节，5000字）
- ✅ 打包最佳实践（8章节，6000字）
- ✅ 版本发布工作流（6章节，4000字）
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
**最后更新**: 2026-02-09
**文档总字数**: ~49,000 字
**文档完整度**: 100%
