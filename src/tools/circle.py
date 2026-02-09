"""圆形工具"""
from PyQt6.QtCore import Qt
from .base_tool import BaseTool
from ..utils.geometry import bresenham_circle, filled_circle
from ..utils.constants import FILL_MODE_OUTLINE, FILL_MODE_FILLED, FILL_MODE_BOTH


class CircleTool(BaseTool):
    """圆形工具"""

    def __init__(self, canvas, fill_mode: str = FILL_MODE_OUTLINE):
        """
        初始化圆形工具

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

        # 计算半径
        radius = self._calculate_radius(start_x, start_y, x, y, modifiers)

        # 更新预览
        self.preview_points = self._get_circle_points(start_x, start_y, radius)
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

        # 计算半径
        radius = self._calculate_radius(start_x, start_y, x, y, modifiers)

        # 绘制圆形
        points = self._get_circle_points(start_x, start_y, radius)
        for px, py in points:
            layer.set_pixel(px, py, True)

        # 重置状态（但不调用 reset()，让 canvas_view 调用 end_draw()）
        self.is_drawing = False
        self.preview_points = []

    def _calculate_radius(self, cx: int, cy: int, x: int, y: int,
                         modifiers: Qt.KeyboardModifier) -> int:
        """
        计算半径

        Args:
            cx, cy: 圆心坐标
            x, y: 当前鼠标坐标
            modifiers: 键盘修饰键

        Returns:
            半径
        """
        dx = x - cx
        dy = y - cy

        # Shift 键锁定为正圆（使用较大的半径）
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            radius = max(abs(dx), abs(dy))
        else:
            # 使用欧几里得距离
            radius = int((dx ** 2 + dy ** 2) ** 0.5)

        return max(1, radius)

    def _get_circle_points(self, cx: int, cy: int, radius: int) -> list[tuple[int, int]]:
        """
        获取圆形的所有点

        Args:
            cx, cy: 圆心坐标
            radius: 半径

        Returns:
            圆形的所有像素坐标列表
        """
        if self.fill_mode == FILL_MODE_OUTLINE:
            return bresenham_circle(cx, cy, radius)
        elif self.fill_mode == FILL_MODE_FILLED:
            return filled_circle(cx, cy, radius)
        elif self.fill_mode == FILL_MODE_BOTH:
            # 先填充，再绘制轮廓
            points = filled_circle(cx, cy, radius)
            points.extend(bresenham_circle(cx, cy, radius))
            return points
        else:
            return bresenham_circle(cx, cy, radius)

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
