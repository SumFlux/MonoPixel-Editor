"""油漆桶填充工具"""
from PyQt6.QtCore import Qt
from .base_tool import BaseTool
from ..utils.geometry import flood_fill


class BucketFillTool(BaseTool):
    """油漆桶填充工具"""

    def __init__(self, canvas):
        """
        初始化油漆桶工具

        Args:
            canvas: 画布对象
        """
        super().__init__(canvas)

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            return

        self.begin_draw()  # 保存当前状态

        # 获取起始点的颜色
        target_value = layer.get_pixel(x, y)
        fill_value = True  # 填充为黑色

        # 如果点击的是黑色像素，则填充为白色
        if target_value:
            fill_value = False

        # 执行泛洪填充
        points = flood_fill(layer.data, x, y, target_value, fill_value)

        # 应用填充
        for px, py in points:
            layer.set_pixel(px, py, fill_value)

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽（填充工具不需要拖拽）"""
        pass

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放"""
        pass
