"""文本工具"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QInputDialog, QFontDialog
from .base_tool import BaseTool
from ..services.text_service import TextService
from ..services.font_manager import FontManager
import numpy as np


class TextTool(BaseTool):
    """文本工具"""

    def __init__(self, canvas):
        """
        初始化文本工具

        Args:
            canvas: 画布对象
        """
        super().__init__(canvas)
        self.font_manager = FontManager()
        self.text_service = TextService(self.font_manager)
        self.current_font = QFont("Arial", 12)
        self.squeeze_halfwidth = True
        self.text_preview = None
        self.preview_pos = None

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        self.begin_draw()  # 保存当前状态

        # 弹出文本输入对话框
        text, ok = QInputDialog.getText(
            None, "输入文本", "文本内容:",
            text=""
        )

        if not ok or not text:
            self.reset()
            return

        # 弹出字体选择对话框
        font, ok = QFontDialog.getFont(self.current_font)
        if ok:
            self.current_font = font

        # 渲染文本
        try:
            text_bitmap = self.text_service.render_text(
                text, self.current_font, self.squeeze_halfwidth
            )

            # 保存预览
            self.text_preview = text_bitmap
            self.preview_pos = (x, y)
            self.is_drawing = True

        except Exception as e:
            print(f"文本渲染失败: {e}")
            self.reset()

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽（移动文本位置）"""
        if self.is_drawing and self.text_preview is not None:
            self.preview_pos = (x, y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放（栅格化文本到图层）"""
        if not self.is_drawing or self.text_preview is None:
            self.reset()
            return

        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            self.reset()
            return

        # 栅格化文本到图层
        px, py = self.preview_pos
        height, width = self.text_preview.shape

        for dy in range(height):
            for dx in range(width):
                if self.text_preview[dy, dx]:
                    layer.set_pixel(px + dx, py + dy, True)

        self.reset()

    def get_preview_points(self) -> list[tuple[int, int]]:
        """获取预览点"""
        if self.text_preview is None or self.preview_pos is None:
            return []

        points = []
        px, py = self.preview_pos
        height, width = self.text_preview.shape

        for dy in range(height):
            for dx in range(width):
                if self.text_preview[dy, dx]:
                    points.append((px + dx, py + dy))

        return points

    def reset(self) -> None:
        """重置工具状态"""
        super().reset()
        self.text_preview = None
        self.preview_pos = None

    def set_squeeze_halfwidth(self, squeeze: bool) -> None:
        """
        设置是否挤压半角字符

        Args:
            squeeze: 是否挤压
        """
        self.squeeze_halfwidth = squeeze
