"""文本渲染服务"""
from PyQt6.QtGui import QFont, QImage, QPainter, QColor
from PyQt6.QtCore import Qt, QRect
import numpy as np
from typing import Tuple

from .font_manager import FontManager


class TextService:
    """文本渲染服务类"""

    def __init__(self, font_manager: FontManager):
        """
        初始化文本渲染服务

        Args:
            font_manager: 字体管理器
        """
        self.font_manager = font_manager

    def render_text(self, text: str, font: QFont, squeeze_halfwidth: bool = True) -> np.ndarray:
        """
        渲染文本为位图

        Args:
            text: 要渲染的文本
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符

        Returns:
            位图数据 (height, width)
        """
        if not text:
            return np.zeros((1, 1), dtype=bool)

        # 创建临时图像以测量文本尺寸
        temp_image = QImage(1, 1, QImage.Format.Format_ARGB32)
        temp_painter = QPainter(temp_image)
        temp_painter.setFont(font)

        # 计算每个字符的宽度
        char_widths = []
        total_width = 0

        for char in text:
            if squeeze_halfwidth and not self.font_manager.is_fullwidth_char(char):
                # 半角字符：智能挤压 45%-55%
                char_width = temp_painter.fontMetrics().horizontalAdvance(char)
                squeeze_ratio = self._calculate_squeeze_ratio(char, char_width, font.pointSize())
                squeezed_width = int(char_width * squeeze_ratio)
                char_widths.append(squeezed_width)
                total_width += squeezed_width
            else:
                # 全角字符：不挤压
                char_width = temp_painter.fontMetrics().horizontalAdvance(char)
                char_widths.append(char_width)
                total_width += char_width

        # 计算总高度
        height = temp_painter.fontMetrics().height()
        temp_painter.end()

        # 创建实际渲染图像
        image = QImage(total_width, height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        painter = QPainter(image)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))

        # 逐字符渲染
        x_offset = 0
        for i, char in enumerate(text):
            char_width = char_widths[i]

            # 绘制字符
            rect = QRect(x_offset, 0, char_width, height)
            painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, char)

            x_offset += char_width

        painter.end()

        # 转换为位图
        bitmap = self._image_to_bitmap(image)

        return bitmap

    def _calculate_squeeze_ratio(self, char: str, char_width: int, font_size: int) -> float:
        """
        计算半角字符的挤压比例（45%-55%）

        Args:
            char: 字符
            char_width: 字符原始宽度
            font_size: 字体大小

        Returns:
            挤压比例（0.45-0.55）
        """
        # 目标宽度：字体大小的 50%
        target_width = font_size * 0.5

        if char_width == 0:
            return 0.5

        # 计算比例
        ratio = target_width / char_width

        # 限制在 45%-55% 范围内
        ratio = max(0.45, min(0.55, ratio))

        return ratio

    def _image_to_bitmap(self, image: QImage) -> np.ndarray:
        """
        将 QImage 转换为位图

        Args:
            image: QImage 对象

        Returns:
            位图数据
        """
        width = image.width()
        height = image.height()

        # 转换为灰度
        bitmap = np.zeros((height, width), dtype=bool)

        for y in range(height):
            for x in range(width):
                pixel = image.pixel(x, y)
                # 提取灰度值（简单平均）
                r = (pixel >> 16) & 0xFF
                g = (pixel >> 8) & 0xFF
                b = pixel & 0xFF
                gray = (r + g + b) // 3

                # 阈值二值化（128）
                bitmap[y, x] = gray < 128

        return bitmap

    def get_text_bounds(self, text: str, font: QFont, squeeze_halfwidth: bool = True) -> Tuple[int, int]:
        """
        获取文本渲染后的尺寸

        Args:
            text: 文本
            font: 字体
            squeeze_halfwidth: 是否挤压半角字符

        Returns:
            (width, height)
        """
        if not text:
            return (0, 0)

        # 创建临时图像以测量
        temp_image = QImage(1, 1, QImage.Format.Format_ARGB32)
        temp_painter = QPainter(temp_image)
        temp_painter.setFont(font)

        # 计算宽度
        total_width = 0
        for char in text:
            if squeeze_halfwidth and not self.font_manager.is_fullwidth_char(char):
                char_width = temp_painter.fontMetrics().horizontalAdvance(char)
                squeeze_ratio = self._calculate_squeeze_ratio(char, char_width, font.pointSize())
                total_width += int(char_width * squeeze_ratio)
            else:
                total_width += temp_painter.fontMetrics().horizontalAdvance(char)

        height = temp_painter.fontMetrics().height()
        temp_painter.end()

        return (total_width, height)
