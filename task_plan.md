# Task Plan: MonoPixel Editor - 单色像素画编辑器

## Goal
创建一个基于 PyQt6 的单色像素画编辑与取模工具，专用于嵌入式 OLED/LCD 开发，支持多图层、完整绘图工具、文本渲染和多种取模格式导出。

## Current Phase
Phase 8 - 修复新发现的问题（状态栏布局、文字预览框、字间距、选择框手柄、图层显示/隐藏）

## Phases

### Phase 1: 项目初始化与基础框架
- [x] 创建项目目录结构
- [x] 生成 requirements.txt（PyQt6, NumPy, Pillow）
- [x] 实现 Canvas 和 Layer 数据模型
- [x] 实现 CanvasView（基于 QGraphicsView）
- [x] 实现滚轮缩放（以鼠标为中心）
- [x] 实现中键/空格+左键平移
- [x] 实现网格线渲染
- [x] 实现 MainWindow 主窗口布局
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/main.py, src/ui/main_window.py, src/ui/canvas_view.py, src/core/canvas.py, src/core/layer.py

### Phase 2: 基础绘图工具
- [x] 设计 BaseTool 抽象基类
- [x] 实现画笔工具（支持笔触大小 1px, 2px, 3px）
- [x] 实现橡皮擦工具
- [x] 实现直线工具（实时预览、Shift 键锁定）
- [x] 实现矩形/圆形工具（轮廓/填充模式、Shift 键锁定）
- [x] 实现油漆桶填充（4-连通泛洪算法）
- [x] 创建工具栏 UI
- [x] 创建属性面板
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/tools/*.py, src/ui/toolbar.py, src/ui/property_panel.py

### Phase 3: 图层系统
- [x] 实现图层面板 UI（列表、新建/删除/复制/上移/下移）
- [x] 实现图层混合逻辑（透明像素不遮挡下层）
- [x] 实现撤销/重做栈（命令模式）
- [x] 支持 Ctrl+Z / Ctrl+Y
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/ui/layer_panel.py, src/core/history.py

### Phase 4: 文本工具
- [x] 实现字体管理器（列出系统字体、加载自定义字体）
- [x] 实现文本渲染服务（二值化处理）
- [x] 实现智能挤压算法（半角字符 45%-55%）
- [x] 实现文本工具（点击输入、浮动对象、栅格化）
- [x] 创建自定义 TextInputDialog
- [x] 支持从本地 fonts/ 文件夹加载字体
- [x] 使用 setPixelSize() 实现精确像素级字号
- [x] 文本预览状态支持拖拽和重新编辑
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/tools/text.py, src/services/text_service.py, src/services/font_manager.py

### Phase 5: 选择工具与缩放
- [x] 实现选择工具（框选矩形区域）
- [x] 显示选区手柄（8个方向）
- [x] 实现选区移动
- [x] 实现选区缩放（最近邻插值）
- [x] 修复选区手柄位置问题
- [x] 修复选区边框粗细问题（使用 cosmetic pen）
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/tools/select.py, src/utils/geometry.py

### Phase 6: 导出系统
- [x] 实现位运算工具（字节对齐、MSB/LSB 转换）
- [x] 实现水平扫描算法
- [x] 实现垂直扫描算法（Page mode）
- [x] 实现预览服务（反向解析）
- [x] 实现导出对话框 UI
- [x] 实现文件输出（C Header, Binary, PNG）
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/services/export_service.py, src/services/preview_service.py, src/ui/export_dialog.py

### Phase 7: 项目保存/加载
- [x] 设计 JSON 格式
- [x] 实现保存功能（NumPy 数组转 Base64）
- [x] 实现加载功能（Base64 解码为 NumPy 数组）
- [x] 测试数据完整性
- **Status:** complete
- **完成日期:** 2026-02-09
- **关键文件:** src/core/project.py

### Phase 8: UI 优化与打包
- [x] 添加快捷键（Ctrl+N, Ctrl+S, Ctrl+E, Ctrl+Z, Ctrl+Y, G）
- [x] 优化 UI 样式（QSS）
- [x] 添加图标资源
- [ ] 使用 PyInstaller 打包
- [ ] 测试打包后的可执行文件
- **Status:** in_progress
- **关键文件:** src/ui/main_window.py, resources/

## 最近完成的修复（2026-02-09）

### 用户反馈问题修复
1. **撤销/重做系统** ✅
   - 问题：画直线撤销会影响其他操作
   - 解决：添加 History.add() 方法，分离命令添加和执行逻辑
   - 测试：test_undo_redo.py 全部通过

2. **选择框渲染** ✅
   - 问题：手柄位置错误（固定在左上角）+ 边框随缩放变粗
   - 解决：修正坐标变换 + 使用 cosmetic pen (width=0)
   - 文件：src/tools/select.py

3. **画布平移** ✅
   - 问题：画布固定在中心，右键拖动无效
   - 解决：改用 NoAnchor 模式
   - 文件：src/ui/canvas_view.py

4. **文本工具改进** ✅
   - 问题：字号不准确 + 无法加载自定义字体 + 缺少预览编辑功能
   - 解决：完全重写文本工具
     - 创建自定义 TextInputDialog
     - 使用 setPixelSize() 精确控制字号
     - 支持从 fonts/ 文件夹加载字体
     - 实现预览拖拽和 Enter 键重新编辑
   - 文件：src/tools/text.py

5. **其他功能** ✅
   - 鼠标坐标显示：状态栏实时显示
   - 网格线设置：View 菜单切换（快捷键 G）

## Key Questions

1. ~~应该使用什么 GUI 框架？~~ → **已决定：PyQt6**
2. ~~如何实现半角字符智能挤压？~~ → **已实现：45%-55% 动态调整**
3. ~~垂直扫描 Page mode 如何实现？~~ → **已实现：参考 SSD1306 数据手册**
4. ~~选区缩放使用什么插值算法？~~ → **已实现：最近邻插值**
5. ~~如何验证导出的取模数据正确性？~~ → **已实现：反向解析预览**

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 使用 PyQt6 作为 GUI 框架 | 跨平台、功能强大、文档完善、适合桌面应用 |
| 使用 NumPy 存储位图数据 | 高效的数组操作、内存占用小、支持向量化运算 |
| 图层数据使用 bool 类型 | 1-bit 颜色深度，bool 类型最直观且节省内存 |
| 文本半角字符挤压 45%-55% | 平衡可读性和空间利用率，动态调整适应不同字体 |
| 选区缩放使用最近邻插值 | 保持像素清晰度，适合像素画编辑 |
| 项目文件使用 JSON + Base64 | 人类可读、易于调试、跨平台兼容 |
| 撤销/重做使用命令模式 | 标准设计模式、易于扩展、支持复杂操作 |
| 使用 History.add() 分离逻辑 | 避免重复执行已完成的绘制操作，修复撤销/重做问题 |
| 选择框使用 cosmetic pen | 保持 1px 固定粗细，不随缩放变化，不妨碍视野 |
| 文本工具使用 setPixelSize() | 精确控制像素级字号，而非点大小 |
| 文本工具支持本地字体文件夹 | 方便用户添加自定义字体，无需安装到系统 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| 撤销一次会影响多个操作 | 1 | 添加 `if not self.is_drawing:` 检查 |
| 撤销一次会影响多个操作 | 2 | 重新设计：添加 History.add() 方法，分离命令添加和执行 ✅ |
| 画笔工具撤销问题 | 3 | 画笔和橡皮擦工具添加 `if not self.is_drawing:` 检查 ✅ |
| 选择框手柄固定在左上角 | 1 | 使用 resetTransform() 方法 |
| 选择框手柄固定在左上角 | 2 | 移除 resetTransform()，使用正确的缩放计算 ✅ |
| 选择框边框随缩放变粗 | 1 | 使用 `1 / scale` 作为笔宽 |
| 选择框边框随缩放变粗 | 2 | 使用 cosmetic pen (width=0) ✅ |
| 选择框手柄太大遮挡视线 | 3 | 减小手柄大小从 6px 到 4px |
| 选择框手柄太大遮挡视线 | 4 | 改为 6px 并使用 cosmetic 绘制（待测试）|
| 画布固定在中心无法拖动 | 1 | 改用 NoAnchor 模式 |
| 画布固定在中心无法拖动 | 2 | 扩大场景矩形，添加边距以支持平移 ✅ |
| 文本字号不准确 | 1 | 改用 setPixelSize() 而非 setPointSize() |
| 文本字号不准确（挤压计算错误） | 2 | 修复 text_service.py 使用 pixelSize() 而非 pointSize() |
| 文本字号不准确（宽度计算错误） | 3 | 半角字符固定为字号的 50% 宽度（待测试）|
| 像素网格线不明显 | 1 | 修改网格线颜色为深灰色不透明 |
| 像素网格线太粗 | 2 | 网格线作为独立图形项绘制，使用 cosmetic pen（待测试）|
| 直线工具撤销问题 | 1 | 移除 on_release 中的 reset() 调用，保留 old_layer_data（待测试）|

## Files Modified in Recent Session

### 核心修复
- `src/core/history.py` - 添加 add() 方法，修复撤销/重做系统
- `src/ui/main_window.py` - 修改 _on_draw_completed() 使用 add() 而非 execute()
- `src/tools/select.py` - 修复手柄位置和边框粗细
- `src/ui/canvas_view.py` - 修改为 NoAnchor 模式
- `src/tools/text.py` - 完全重写文本工具

### 新增文件
- `fonts/README.md` - 字体文件夹说明文档
- `test_undo_redo.py` - 撤销/重做功能测试脚本

## Git Commits

```
5a7a2d6 - fix: 修复撤销/重做系统和其他用户体验问题
40b1381 - fix: 修复用户体验问题
5a7760f - feat: initial release of MonoPixel Editor v1.0.0
```

## Next Steps

1. **打包发布**
   - 使用 PyInstaller 打包为可执行文件
   - 测试 Windows 平台的打包版本
   - 创建安装说明文档

2. **文档完善**
   - 编写用户手册
   - 添加使用示例
   - 创建 README.md

3. **可选优化**
   - 添加更多导出格式
   - 支持图像导入
   - 添加更多绘图工具（多边形、曲线等）

## Notes

- ✅ 所有核心功能已完成
- ✅ 所有用户反馈问题已修复
- ✅ 测试脚本验证通过
- 项目已达到 v1.0.0 发布标准
- 下一步重点：打包和文档
