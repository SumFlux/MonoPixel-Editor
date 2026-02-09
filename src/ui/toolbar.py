"""工具栏组件"""
from PyQt6.QtWidgets import (
    QToolBar, QButtonGroup, QToolButton, QLabel, QWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

from ..utils.constants import (
    TOOL_PENCIL, TOOL_ERASER, TOOL_LINE, TOOL_RECTANGLE,
    TOOL_CIRCLE, TOOL_BUCKET_FILL, TOOL_SELECT, TOOL_TEXT
)


class Toolbar(QToolBar):
    """工具栏类"""

    tool_changed = pyqtSignal(str)  # 工具切换信号

    def __init__(self):
        """初始化工具栏"""
        super().__init__()
        self.setWindowTitle("工具")
        self.setOrientation(Qt.Orientation.Vertical)
        self.setMovable(False)

        # 工具按钮组（单选）
        self.tool_group = QButtonGroup(self)
        self.tool_group.setExclusive(True)

        # 创建工具按钮
        self._create_tools()

        # 默认选中画笔工具
        self.current_tool = TOOL_PENCIL

    def _create_tools(self) -> None:
        """创建工具按钮"""
        tools = [
            (TOOL_PENCIL, "画笔 (1)", "画笔工具"),
            (TOOL_ERASER, "橡皮擦 (2)", "橡皮擦工具"),
            (TOOL_LINE, "直线 (3)", "直线工具"),
            (TOOL_RECTANGLE, "矩形 (4)", "矩形工具"),
            (TOOL_CIRCLE, "圆形 (5)", "圆形工具"),
            (TOOL_BUCKET_FILL, "填充 (6)", "油漆桶填充工具"),
            (TOOL_SELECT, "选择 (7)", "选择工具"),
            (TOOL_TEXT, "文本 (8)", "文本工具"),
        ]

        for i, (tool_id, text, tooltip) in enumerate(tools):
            button = QToolButton()
            button.setText(text)
            button.setToolTip(tooltip)
            button.setCheckable(True)
            button.setProperty("tool_id", tool_id)

            # 设置快捷键（数字键 1-8）
            button.setShortcut(str(i + 1))

            # 添加到按钮组
            self.tool_group.addButton(button, i)

            # 连接信号
            button.clicked.connect(lambda checked, tid=tool_id: self._on_tool_clicked(tid))

            # 添加到工具栏
            self.addWidget(button)

            # 默认选中画笔
            if tool_id == TOOL_PENCIL:
                button.setChecked(True)

    def _on_tool_clicked(self, tool_id: str) -> None:
        """
        工具按钮点击事件

        Args:
            tool_id: 工具 ID
        """
        self.current_tool = tool_id
        self.tool_changed.emit(tool_id)

    def get_current_tool(self) -> str:
        """
        获取当前选中的工具

        Returns:
            工具 ID
        """
        return self.current_tool

    def set_tool(self, tool_id: str) -> None:
        """
        设置当前工具

        Args:
            tool_id: 工具 ID
        """
        for button in self.tool_group.buttons():
            if button.property("tool_id") == tool_id:
                button.setChecked(True)
                self.current_tool = tool_id
                self.tool_changed.emit(tool_id)
                break
