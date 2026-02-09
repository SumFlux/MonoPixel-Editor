"""矩形工具"""
from PyQt6.QtCore import Qt
from .base_tool import BaseTool
from ..utils.geometry import rectangle_outline, filled_rectangle, make_square
from ..utils.constants import FILL_MODE_OUTLINE, FILL_MODE_FILLED, FILL_MODE_BOTH


class RectangleTool(BaseTool):
    """矩形工具"""

    def __init__(self, canvas, fill_mode: str = FILL_MODE_OUTLINE):
        """
        初始化矩形工具

        Args:
            canvas: 画布对象
            fill_mode: 填充模式（outline/filled/both）
        """
        super().__init__(canvas)
        self.fill_mode = fill_mode
        self.preview_points = []

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        if not self.is_drawing:
            self.begin_draw()  # 只在开始新绘制时保存状态
        self.is_drawing = True
        self.start_pos = (x, y)
        self.last_pos = (x, y)
        self.preview_points = [(x, y)]

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽"""
        if not self.is_drawing or self.start_pos is None:
            return

        start_x, start_y = self.start_pos

        # Shift 键锁定为正方形
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            x, y = make_square(start_x, start_y, x, y)

        # 更新预览
        self.preview_points = self._get_rectangle_points(start_x, start_y, x, y)
        self.last_pos = (x, y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放"""
        if not self.is_drawing or self.start_pos is None:
            return

        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            self.reset()
            return

        start_x, start_y = self.start_pos

        # Shift 键锁定为正方形
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            x, y = make_square(start_x, start_y, x, y)

        # 绘制矩形
        points = self._get_rectangle_points(start_x, start_y, x, y)
        for px, py in points:
            layer.set_pixel(px, py, True)

        self.reset()

    def _get_rectangle_points(self, x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
        """
        获取矩形的所有点

        Args:
            x0, y0: 起点坐标
            x1, y1: 终点坐标

        Returns:
            矩形的所有像素坐标列表
        """
        if self.fill_mode == FILL_MODE_OUTLINE:
            return rectangle_outline(x0, y0, x1, y1)
        elif self.fill_mode == FILL_MODE_FILLED:
            return filled_rectangle(x0, y0, x1, y1)
        elif self.fill_mode == FILL_MODE_BOTH:
            # 先填充，再绘制轮廓（确保轮廓可见）
            points = filled_rectangle(x0, y0, x1, y1)
            points.extend(rectangle_outline(x0, y0, x1, y1))
            return points
        else:
            return rectangle_outline(x0, y0, x1, y1)

    def set_fill_mode(self, mode: str) -> None:
        """
        设置填充模式

        Args:
            mode: 填充模式
        """
        self.fill_mode = mode

    def get_preview_points(self) -> list[tuple[int, int]]:
        """获取预览点"""
        return self.preview_points

    def reset(self) -> None:
        """重置工具状态"""
        super().reset()
        self.preview_points = []
