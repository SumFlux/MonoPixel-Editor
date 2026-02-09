"""画笔工具"""
from PyQt6.QtCore import Qt
from .base_tool import BaseTool
from ..utils.geometry import bresenham_line


class PencilTool(BaseTool):
    """画笔工具"""

    def __init__(self, canvas, brush_size: int = 1):
        """
        初始化画笔工具

        Args:
            canvas: 画布对象
            brush_size: 笔触大小
        """
        super().__init__(canvas)
        self.brush_size = brush_size

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        self.begin_draw()  # 保存当前状态
        self.is_drawing = True
        self.start_pos = (x, y)
        self.last_pos = (x, y)

        # 绘制起始点
        self._draw_point(x, y)

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽"""
        if not self.is_drawing or self.last_pos is None:
            return

        # 从上一个点到当前点绘制直线（实现连续绘制）
        last_x, last_y = self.last_pos
        points = bresenham_line(last_x, last_y, x, y)

        for px, py in points:
            self._draw_point(px, py)

        self.last_pos = (x, y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放"""
        self.is_drawing = False
        self.last_pos = None

    def _draw_point(self, x: int, y: int) -> None:
        """
        绘制一个点（考虑笔触大小）

        Args:
            x, y: 中心坐标
        """
        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            return

        # 根据笔触大小绘制
        radius = self.brush_size // 2

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                # 圆形笔触
                if dx * dx + dy * dy <= radius * radius:
                    layer.set_pixel(x + dx, y + dy, True)

    def set_brush_size(self, size: int) -> None:
        """
        设置笔触大小

        Args:
            size: 笔触大小
        """
        self.brush_size = max(1, size)
