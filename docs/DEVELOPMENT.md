# MonoPixel Editor 开发文档

## 目录

1. [项目架构](#项目架构)
2. [开发环境设置](#开发环境设置)
3. [代码结构](#代码结构)
4. [核心模块详解](#核心模块详解)
5. [工具开发指南](#工具开发指南)
6. [测试指南](#测试指南)
7. [代码规范](#代码规范)
8. [贡献指南](#贡献指南)

---

## 项目架构

### 技术栈

- **GUI 框架**: PyQt6 6.6.0+
- **数组处理**: NumPy 1.24.0+
- **图像处理**: Pillow 10.0.0+
- **测试框架**: pytest 7.4.0+
- **打包工具**: PyInstaller 5.0+

### 架构模式

MonoPixel Editor 采用 **MVC (Model-View-Controller)** 架构：

```
┌─────────────────────────────────────────┐
│              View Layer                 │
│  (UI Components - PyQt6 Widgets)        │
│  - MainWindow                           │
│  - CanvasView                           │
│  - Toolbar, Panels, Dialogs             │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│           Controller Layer              │
│  (Event Handlers & Business Logic)      │
│  - Tool Classes                         │
│  - Services                             │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│             Model Layer                 │
│  (Data Models & Core Logic)             │
│  - Canvas                               │
│  - Layer                                │
│  - History                              │
│  - Project                              │
└─────────────────────────────────────────┘
```

### 设计模式

1. **命令模式 (Command Pattern)**
   - 用于撤销/重做系统
   - 每个操作封装为 Command 对象
   - 文件: `src/core/history.py`

2. **策略模式 (Strategy Pattern)**
   - 用于工具系统
   - 每个工具实现 BaseTool 接口
   - 文件: `src/tools/base_tool.py`

3. **观察者模式 (Observer Pattern)**
   - 用于 UI 更新
   - PyQt6 信号/槽机制
   - 示例: `draw_completed.emit()`

---

## 开发环境设置

### 1. 克隆项目

```bash
git clone <repository-url>
cd 6_MonoPixel_Editor
```

### 2. 创建虚拟环境

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` 内容：
```
pytest>=7.4.0
pytest-qt>=4.2.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

### 5. 配置 IDE

**推荐 IDE**: PyCharm, VS Code

**VS Code 配置** (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

---

## 代码结构

### 目录树

```
6_MonoPixel_Editor/
├── src/                          # 源代码
│   ├── main.py                   # 应用入口
│   ├── core/                     # 核心数据模型
│   │   ├── __init__.py
│   │   ├── canvas.py             # 画布模型
│   │   ├── layer.py              # 图层模型
│   │   ├── history.py            # 历史记录（命令模式）
│   │   └── project.py            # 项目管理
│   ├── tools/                    # 绘图工具
│   │   ├── __init__.py
│   │   ├── base_tool.py          # 工具基类
│   │   ├── pencil.py             # 画笔工具
│   │   ├── eraser.py             # 橡皮擦工具
│   │   ├── line.py               # 直线工具
│   │   ├── rectangle.py          # 矩形工具
│   │   ├── circle.py             # 圆形工具
│   │   ├── bucket_fill.py        # 填充工具
│   │   ├── select.py             # 选择工具
│   │   └── text.py               # 文本工具
│   ├── ui/                       # UI 视图层
│   │   ├── __init__.py
│   │   ├── main_window.py        # 主窗口
│   │   ├── canvas_view.py        # 画布视图
│   │   ├── toolbar.py            # 工具栏
│   │   ├── property_panel.py     # 属性面板
│   │   ├── layer_panel.py        # 图层面板
│   │   ├── export_dialog.py      # 导出对话框
│   │   └── style.qss             # 样式表
│ces/                 # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── export_service.py     # 导出服务
│   │   ├── text_service.py       # 文本渲染服务
│   │   ├── font_manager.py       # 字体管理
│   │   └── preview_service.py    # 预览服务
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       ├── bit_operations.py     # 位运算
│       ├── geometry.py           # 几何计算
│       └── constants.py          # 常量定义
├── tests/                        # 测试代码
│   ├── __init__.py
│   ├── unit/                     # 单元测试
│   │   ├── test_canvas.py
│   │   ├── test_layer.py
│   │   ├── test_history.py
│   │   ├── test_export_service.py
│   │   ├── test_text_service.py
│   │   └── test_select_tool.py
│   └── integration/              # 集成测试
│       └── test_workflow.py
├── docs/                         # 文档
│   ├── USER_MANUAL.md            # 用户手册
│   ├── DEVELOPMENT.md            # 开发文档（本文件）
│   └── BUILD_GUIDE.md            # 打包发布指南
├── MonoPixelEditor.spec          # PyInstaller 配置
├── build.bat                     # 打包脚本（Windows）
├── requirements.txt              # 运行依赖
├── requirements-dev.txt          # 开发依赖
└── README.md                     # 项目说明
```

---

## 核心模块详解

### 1. Canvas (画布模型)

**文件**: `src/core/canvas.py`

**职责**:
- 管理画布尺寸
- 管理多个图层
- 合并可见图层
- 网格线显示控制

**核心方法**:

```python
class Canvas:
    def __init__(self, width: int, height: int):
        """初始化画布"""

    def add_layer(self, name: str = None) -> Layer:
        """添加新图层"""

    def remove_layer(self, index: int) -> None:
        """删除图层"""

    def merge_visible_layers(self) -> np.ndarray:
        """合并所有可见图层"""

    def get_active_layer(self) -> Optional[Layer]:
        """获取当前活动图层"""
```

**数据结构**:
```python
{
    'width': int,           # 画布宽度
    'height': int,          # 画布高度
    'layers': List[Layer],  # 图层列表
    'active_layer_index': int,  # 活动图层索引
    'grid_visible': bool    # 网格线是否可见
}
```

### 2. Layer (图层模型)

**文件**: `src/core/layer.py`

**职责**:
- 存储图层像素数据
- 提供像素读写接口
- 管理图层属性

**核心方法**:

```python
class Layer:
    def __init__(self, width: int, height: int, name: str = "Layer"):
        """初始化图层"""

    def set_pixel(self, x: int, y: int, value: bool) -> None:
        """设置像素值"""

    def get_pixel(self, x: int, y: int) -> bool:
        """获取像素值"""

    def clear(self) -> None:
        """清空图层"""

    def copy(self) -> 'Layer':
        """复制图层"""
```

**数据结构**:
```python
{
    'name': str,                    # 图层名称
    'data': np.ndarray,             # 像素数据 (height, width), dtype=bool
    'visible': bool,                # 是否可见
    'locked': bool,                 # 是否锁定
    'width': int,                   # 宽度
    'height': int                   # 高度
}
```

**像素数据格式**:
- 使用 NumPy 布尔数组
- `True` = 黑色像素
- `False` = 白色像素（透明）
- 形状: `(height, width)`

### 3. History (历史记录)

**文件**: `src/core/history.py`

**职责**:
- 管理撤销/重做栈
- 执行命令
- 限制历史记录大小

**命令模式实现**:

```python
class Command(ABC):
    """命令抽象基类"""

    @abstractmethod
    def execute(self) -> None:
        """执行命令"""

    @abstractmethod
    def undo(self) -> None:
        """撤销命令"""

class DrawCommand(Command):
    """绘图命令"""

    def __init__(self, layer: Layer, old_data: np.ndarray, new_data: np.ndarray):
        self.layer = layer
        self.old_data = old_data
        self.new_data = new_data

    def execute(self) -> None:
        self.layer.data = self.new_data.copy()

    def undo(self) -> None:
        self.layer.data = self.old_data.copy()
```

**核心方法**:

```python
class History:
    def __init__(self, max_size: int = 50):
        """初始化历史记录"""

    def execute(self, command: Command) -> None:
        """执行命令并添加到历史"""

    def undo(self) -> bool:
        """撤销上一个命令"""

    def redo(self) -> bool:
        """重做下一个命令"""

    def can_undo(self) -> bool:
        """是否可以撤销"""

    def can_redo(self) -> bool:
        """是否可以重做"""
```

### 4. Project (项目管理)

**文件**: `src/core/project.py`

**职责**:
- 保存/加载项目文件
- 管理项目修改状态
- JSON + Base64 编码

**文件格式** (.mpx):

```json
{
    "version": "1.0",
    "canvas": {
        "width": 212,
        "height": 104
    },
    "layers": [
        {
            "name": "Layer 1",
            "visible": true,
            "locked": false,
            "data": "base64_encoded_bitmap_data"
        }
    ]
}
```

**核心方法**:

```python
class Project:
    def save(self, file_path: str) -> bool:
        """保存项目到文件"""

    def load(self, file_path: str) -> bool:
        """从文件加载项目"""

    def mark_modified(self) -> None:
        """标记项目已修改"""

    def is_modified(self) -> bool:
        """检查项目是否已修改"""
```

---

## 工具开发指南

### 创建新工具

所有工具必须继承 `BaseTool` 类并实现其抽象方法。

**步骤 1: 创建工具类**

```python
# src/tools/my_tool.py

from .base_tool import BaseTool
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
import numpy as np

class MyTool(BaseTool):
    """我的自定义工具"""

    def __init__(self, canvas):
        super().__init__(canvas)
        # 初始化工具特定的属性
        self.my_property = None

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下事件"""
        self.is_drawing = True
        self.begin_draw()  # 保存当前图层状态
        self.start_pos = (x, y)

        # 实现工具逻辑
        layer = self.canvas.get_active_layer()
        if layer and not layer.locked:
            layer.set_pixel(x, y, True)

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽事件"""
        if not self.is_drawing:
            return

        # 实现拖拽逻辑
        layer = self.canvas.get_active_layer()
        if layer and not layer.locked:
            layer.set_pixel(x, y, True)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放事件"""
        self.is_drawing = False
        # end_draw() 会在 CanvasView 中调用

    def get_cursor(self) -> QCursor:
        """获取工具光标"""
        return QCursor(Qt.CursorShape.CrossCursor)

    def get_preview_points(self) -> list[tuple[int, int]]:
        """获取预览点（可选）"""
        return []
```

**步骤 2: 注册工具**

在 `src/utils/constants.py` 中添加工具常量：

```python
TOOL_MY_TOOL = "my_tool"
```

在 `src/ui/main_window.py` 中注册工具：

```python
from ..tools.my_tool import MyTool

class MainWindow(QMainWindow):
    def _create_tools(self) -> None:
        self.tools = {
            # ... 其他工具
            TOOL_MY_TOOL: MyTool(self.canvas),
        }
```

**步骤 3: 添加到工具栏**

在 `src/ui/toolbar.py` 中添加工具按钮：

```python
my_tool_btn = QToolButton()
my_tool_btn.setText("我的工具")
my_tool_btn.setCheckable(True)
my_tool_btn.clicked.connect(lambda: self._on_tool_clicked(TOOL_MY_TOOL))
self.addWidget(my_tool_btn)
```

**步骤 4: 编写测试**

```python
# tests/unit/test_my_tool.py

import pytest
from src.core.canvas import Canvas
from src.tools.my_tool import MyTool

@pytest.fixture
def canvas():
    return Canvas(20, 20)

@pytest.fixture
def my_tool(canvas):
    return MyTool(canvas)

def test_my_tool_init(my_tool):
    """测试工具初始化"""
    assert my_tool.my_property is None

def test_my_tool_draw(canvas, my_tool):
    """测试绘制功能"""
    layer = canvas.get_active_layer()

    my_tool.on_press(5, 5, Qt.KeyboardModifier.NoModifier)
    my_tool.on_release(5, 5, Qt.KeyboardModifier.NoModifier)

    assert layer.get_pixel(5, 5) == True
```

### 工具开发最佳实践

1. **始终检查图层锁定状态**
   ```python
   layer = self.canvas.get_active_layer()
   if layer and not layer.locked:
       # 执行绘制操作
   ```

2. **使用 begin_draw() 和 end_draw()**
   - `begin_draw()`: 在开始绘制前调用，保存图层状态
   - `end_draw()`: 在 CanvasView 中自动调用，返回旧数据和新数据

3. **边界检查**
   ```python
   if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
       layer.set_pixel(x, y, True)
   ```

4. **支持修饰键**
   ```python
   shift_pressed = modifiers & Qt.KeyboardModifier.ShiftModifier
   if shift_pressed:
       # 特殊行为（如锁定角度）
   ```

5. **提供预览**
   ```python
   def get_preview_points(self) -> list[tuple[int, int]]:
       """返回预览点列表"""
       if self.is_drawing and self.start_pos:
           return [(self.start_pos[0], self.start_pos[1])]
       return []
   ```

---

## 测试指南

### 测试框架

使用 **pytest** 进行单元测试和集成测试。

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/ -v

# 运行特定测试文件
pytest tests/unit/test_canvas.py -v

# 运行特定测试函数
pytest tests/unit/test_canvas.py::test_canvas_init -v

# 生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

### 编写单元测试

**测试文件命名**: `test_<module_name>.py`

**测试函数命名**: `test_<function_name>_<scenario>`

**示例**:

```python
# tests/unit/test_canvas.py

import pytest
import numpy as np
from src.core.canvas import Canvas

@pytest.fixture
def canvas():
    """创建测试画布"""
    return Canvas(20, 20)

def test_canvas_init(canvas):
    """测试画布初始化"""
    assert canvas.width == 20
    assert canvas.height == 20
    assert len(canvas.layers) == 1
    assert canvas.active_layer_index == 0

def test_add_layer(canvas):
    """测试添加图层"""
    initial_count = len(canvas.layers)
    canvas.add_layer("New Layer")
    assert len(canvas.layers) == initial_count + 1
    assert canvas.layers[-1].name == "New Layer"

def test_merge_visible_layers(canvas):
    """测试合并可见图层"""
    # 在第一个图层绘制
    canvas.layers[0].set_pixel(5, 5, True)

    # 添加第二个图层并绘制
    canvas.add_layer()
    canvas.layers[1].set_pixel(10, 10, True)

    # 合并
    merged = canvas.merge_visible_layers()

    assert merged[5, 5] == True
    assert merged[10, 10] == True
```

### 测试覆盖率目标

- **总体覆盖率**: ≥ 80%
- **核心模块**: ≥ 90%
  - `src/core/`
  - `src/tools/`
  - `src/services/`

### 集成测试

```python
# tests/integration/test_workflow.py

def test_complete_drawing_workflow(qtbot):
    """测试完整的绘图工作流"""
    from src.ui.main_window import MainWindow

    # 创建主窗口
    window = MainWindow()
    qtbot.addWidget(window)

    # 选择画笔工具
    window._set_tool(TOOL_PENCIL)

    # 模拟绘制
    canvas_view = window.canvas_view
    # ... 模拟鼠标事件

    # 验证结果
    layer = window.canvas.get_active_layer()
    assert layer.get_pixel(10, 10) == True
```

---

## 代码规范

### Python 代码风格

遵循 **PEP 8** 规范，使用 **Black** 格式化工具。

**配置** (`pyproject.toml`):

```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

**运行格式化**:

```bash
black src/ tests/
```

### 命名规范

- **类名**: PascalCase (例如: `CanvasView`, `BaseTool`)
- **函数名**: snake_case (例如: `get_active_layer`, `on_press`)
- **常量**: UPPER_SNAKE_CASE (例如: `TOOL_PENCIL`, `MAX_ZOOM`)
- **私有方法**: 前缀 `_` (例如: `_create_menu_bar`)

### 文档字符串

使用 **Google 风格** 文档字符串：

```python
def merge_visible_layers(self) -> np.ndarray:
    """
    合并所有可见图层

    从下到上依次叠加可见图层，黑色像素遮挡下层，
    白色像素透明。

    Returns:
        np.ndarray: 合并后的像素数据，形状为 (height, width)

    Example:
        >>> canvas = Canvas(100, 100)
        >>> merged = canvas.merge_visible_layers()
        >>> print(merged.shape)
        (100, 100)
    """
    # 实现代码
```

### 类型注解

使用 Python 类型注解提高代码可读性：

```python
from typing import Optional, List, Tuple

def add_layer(self, name: Optional[str] = None) -> Layer:
    """添加新图层"""
    if name is None:
        name = f"Layer {len(self.layers) + 1}"
    layer = Layer(self.width, self.height, name)
    self.layers.append(layer)
    return layer
```

### 错误处理

```python
def load(self, file_path: str) -> bool:
    """加载项目文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 处理数据
        return True
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"JSON 解析失败: {file_path}")
        return False
    except Exception as e:
        print(f"加载失败: {e}")
        return False
```

---

## 贡献指南

### 提交代码流程

1. **Fork 项目**
   ```bash
   git clone https://github.com/your-username/MonoPixelEditor.git
   cd MonoPixelEditor
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **编写代码**
   - 遵循代码规范
   - 编写测试
   - 更新文档

4. **运行测试**
   ```bash
   pytest tests/
   black src/ tests/
   flake8 src/ tests/
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add my new feature"
   ```

6. **推送分支**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 描述更改内容
   - 等待代码审查

### 提交信息规范

使用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**:
```
feat(tools): add polygon tool

- Implement polygon drawing with multiple points
- Support fill modes (outline, fill, both)
- Add unit tests

Closes #123
```

### 代码审查清单

- [ ] 代码遵循 PEP 8 规范
- [ ] 所有函数有文档字符串
- [ ] 添加了单元测试
- [ ] 测试覆盖率 ≥ 80%
- [ ] 没有引入新的警告
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确

---

## 常见开发任务

### 添加新的导出格式

1. 在 `src/services/export_service.py` 中添加导出方法
2. 在 `src/ui/export_dialog.py` 中添加格式选项
3. 编写单元测试
4. 更新用户手册

### 添加新的快捷键

1. 在 `src/ui/main_window.py` 的 `_create_menu_bar()` 中添加
2. 或在 `keyPressEvent()` 中处理
3. 更新 README.md 快捷键列表

### 修改 UI 样式

1. 编辑 `src/ui/style.qss`
2. 重启应用查看效果
3. 确保所有控件样式一致

---

## 性能优化建议

### 1. NumPy 向量化

**避免**:
```python
for y in range(height):
    for x in range(width):
        if data[y, x]:
            result[y, x] = True
```

**推荐**:
```python
result = data.copy()
```

### 2. 缓存计算结果

```python
@lru_cache(maxsize=128)
def calculate_expensive_value(param):
    # 昂贵的计算
    return result
```

### 3. 延迟加载

```python
class MyClass:
    def __init__(self):
        self._expensive_resource = None

    @property
    def expensive_resource(self):
        if self._expensive_resource is None:
            self._expensive_resource = load_resource()
        return self._expensive_resource
```

---

## 调试技巧

### 1. 使用 Python 调试器

```python
import pdb; pdb.set_trace()
```

### 2. 日志记录

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### 3. PyQt6 调试

```python
# 打印对象树
def print_widget_tree(widget, indent=0):
    print("  " * indent + widget.__class__.__name__)
    for child in widget.children():
        print_widget_tree(child, indent + 1)
```

---

## 参考资源

- [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [NumPy 文档](https://numpy.org/doc/)
- [pytest 文档](https://docs.pytest.org/)
- [PEP 8 风格指南](https://pep8.org/)
- [Python 类型注解](https://docs.python.org/3/library/typing.html)

---

**MonoPixel Editor Development Team**
© 2024 MonoPixel. All rights reserved.
