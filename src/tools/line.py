"""直线工具"""
from PyQt6.QtCore import Qt
from .base_tool import BaseTool
from ..utils.geometry import bresenham_line, snap_to_angle


class LineTool(BaseTool):
    """直线工具"""

    def __init__(self, canvas):
        """
        初始化直线工具

        Args:
            canvas: 画布对象
        """
        super().__init__(canvas)
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

        # Shift 键锁定角度
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            x, y = snap_to_angle(start_x, start_y, x, y)

        # 更新预览
        self.preview_points = bresenham_line(start_x, start_y, x, y)
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

        # Shift 键锁定角度
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            x, y = snap_to_angle(start_x, start_y, x, y)

        # 绘制直线
        points = bresenham_line(start_x, start_y, x, y)
        for px, py in points:
            layer.set_pixel(px, py, True)

        self.reset()

    def get_preview_points(self) -> list[tuple[int, int]]:
        """获取预览点"""
        return self.preview_points

    def reset(self) -> None:
        """重置工具状态"""
        super().reset()
        self.preview_points = []
