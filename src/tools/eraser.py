"""橡皮擦工具"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from .base_tool import BaseTool
from ..utils.geometry import bresenham_line


class EraserTool(BaseTool):
    """橡皮擦工具"""

    def __init__(self, canvas, eraser_size: int = 1):
        """
        初始化橡皮擦工具

        Args:
            canvas: 画布对象
            eraser_size: 橡皮擦大小
        """
        super().__init__(canvas)
        self.eraser_size = eraser_size

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        self.begin_draw()  # 保存当前状态
        self.is_drawing = True
        self.start_pos = (x, y)
        self.last_pos = (x, y)

        # 擦除起始点
        self._erase_point(x, y)

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽"""
        if not self.is_drawing or self.last_pos is None:
            return

        # 从上一个点到当前点擦除
        last_x, last_y = self.last_pos
        points = bresenham_line(last_x, last_y, x, y)

        for px, py in points:
            self._erase_point(px, py)

        self.last_pos = (x, y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放"""
        self.is_drawing = False
        self.last_pos = None

    def _erase_point(self, x: int, y: int) -> None:
        """
        擦除一个点（考虑橡皮擦大小）

        Args:
            x, y: 中心坐标
        """
        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            return

        # 根据橡皮擦大小擦除
        radius = self.eraser_size // 2

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                # 圆形橡皮擦
                if dx * dx + dy * dy <= radius * radius:
                    layer.set_pixel(x + dx, y + dy, False)

    def set_eraser_size(self, size: int) -> None:
        """
        设置橡皮擦大小

        Args:
            size: 橡皮擦大小
        """
        self.eraser_size = max(1, size)

    def get_cursor(self) -> QCursor:
        """获取光标"""
        return QCursor(Qt.CursorShape.CrossCursor)
