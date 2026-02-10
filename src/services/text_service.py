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

    def render_text(
        self,
        text: str,
        font: QFont,
        squeeze_halfwidth: bool = True,
        max_width: int = 0,
        letter_spacing: int = 0,
        line_spacing: int = 0
    ) -> np.ndarray:
        """
        渲染文本为位图

        Args:
            text: 要渲染的文本
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符
            max_width: 最大宽度（0 = 不限制）
            letter_spacing: 字间距（像素）
            line_spacing: 行间距（像素）

        Returns:
            位图数据 (height, width)
        """
        if not text:
            return np.zeros((1, 1), dtype=bool)

        # 如果设置了最大宽度，进行自动换行
        if max_width > 0:
            lines = self._wrap_text(text, font, squeeze_halfwidth, letter_spacing, max_width)
        else:
            lines = [text]

        # 渲染多行文本
        if len(lines) == 1:
            return self._render_single_line(lines[0], font, squeeze_halfwidth, letter_spacing)
        else:
            return self._render_multiline(lines, font, squeeze_halfwidth, letter_spacing, line_spacing)

    def _calculate_squeeze_ratio(self, char: str, char_width: int, font_size: int) -> float:
        """
        计算半角字符的挤压比例（45%-55%）

        Args:
            char: 字符
            char_width: 字符原始宽度
            font_size: 字体大小（像素）

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

    def _wrap_text(
        self,
        text: str,
        font: QFont,
        squeeze_halfwidth: bool,
        letter_spacing: int,
        max_width: int
    ) -> list[str]:
        """
        将文本按最大宽度分行

        Args:
            text: 文本内容
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符
            letter_spacing: 字间距
            max_width: 最大宽度

        Returns:
            文本行列表
        """
        lines = []
        current_line = ""
        current_width = 0

        for char in text:
            char_width = self._calculate_char_width(char, font, squeeze_halfwidth)
            char_width_with_spacing = char_width + letter_spacing

            if current_width + char_width > max_width and current_line:
                # 超过最大宽度，换行
                lines.append(current_line)
                current_line = char
                current_width = char_width
            else:
                current_line += char
                current_width += char_width_with_spacing

        if current_line:
            lines.append(current_line)

        return lines

    def _calculate_char_width(self, char: str, font: QFont, squeeze_halfwidth: bool) -> int:
        """
        计算单个字符的宽度

        Args:
            char: 字符
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符

        Returns:
            字符宽度（像素）
        """
        if squeeze_halfwidth and not self.font_manager.is_fullwidth_char(char):
            # 半角字符：固定为字号的 50% 宽度
            font_size = font.pixelSize() if font.pixelSize() > 0 else font.pointSize()
            return int(font_size * 0.5)
        else:
            # 全角字符：使用实际宽度
            temp_image = QImage(1, 1, QImage.Format.Format_ARGB32)
            temp_painter = QPainter(temp_image)
            temp_painter.setFont(font)
            char_width = temp_painter.fontMetrics().horizontalAdvance(char)
            temp_painter.end()
            return char_width

    def _render_single_line(
        self,
        text: str,
        font: QFont,
        squeeze_halfwidth: bool,
        letter_spacing: int
    ) -> np.ndarray:
        """
        渲染单行文本

        Args:
            text: 文本内容
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符
            letter_spacing: 字间距

        Returns:
            位图数据
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

        for i, char in enumerate(text):
            char_width = self._calculate_char_width(char, font, squeeze_halfwidth)
            char_widths.append(char_width)
            total_width += char_width
            # 添加字间距（最后一个字符不添加）
            if i < len(text) - 1:
                total_width += letter_spacing

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
            # 添加字间距（最后一个字符不添加）
            if i < len(text) - 1:
                x_offset += letter_spacing

        painter.end()

        # 转换为位图
        bitmap = self._image_to_bitmap(image)

        return bitmap

    def _render_multiline(
        self,
        lines: list[str],
        font: QFont,
        squeeze_halfwidth: bool,
        letter_spacing: int,
        line_spacing: int
    ) -> np.ndarray:
        """
        渲染多行文本

        Args:
            lines: 文本行列表
            font: 字体对象
            squeeze_halfwidth: 是否挤压半角字符
            letter_spacing: 字间距
            line_spacing: 行间距

        Returns:
            位图数据
        """
        if not lines:
            return np.zeros((1, 1), dtype=bool)

        # 渲染每一行
        line_bitmaps = []
        max_width = 0

        for line in lines:
            line_bitmap = self._render_single_line(line, font, squeeze_halfwidth, letter_spacing)
            line_bitmaps.append(line_bitmap)
            max_width = max(max_width, line_bitmap.shape[1])

        # 计算总高度
        line_height = line_bitmaps[0].shape[0]
        total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)

        # 创建结果位图
        result = np.zeros((total_height, max_width), dtype=bool)

        # 垂直拼接所有行
        y_offset = 0
        for line_bitmap in line_bitmaps:
            line_h, line_w = line_bitmap.shape
            result[y_offset:y_offset + line_h, :line_w] = line_bitmap
            y_offset += line_h + line_spacing

        return result

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

    def get_text_bounds(
        self,
        text: str,
        font: QFont,
        squeeze_halfwidth: bool = True,
        max_width: int = 0,
        letter_spacing: int = 0,
        line_spacing: int = 0
    ) -> Tuple[int, int]:
        """
        获取文本渲染后的尺寸

        Args:
            text: 文本
            font: 字体
            squeeze_halfwidth: 是否挤压半角字符
            max_width: 最大宽度（0 = 不限制）
            letter_spacing: 字间距
            line_spacing: 行间距

        Returns:
            (width, height)
        """
        if not text:
            return (0, 0)

        # 如果设置了最大宽度，进行自动换行
        if max_width > 0:
            lines = self._wrap_text(text, font, squeeze_halfwidth, letter_spacing, max_width)
        else:
            lines = [text]

        # 创建临时图像以测量
        temp_image = QImage(1, 1, QImage.Format.Format_ARGB32)
        temp_painter = QPainter(temp_image)
        temp_painter.setFont(font)

        # 计算每行的宽度，取最大值
        max_line_width = 0
        for line in lines:
            line_width = 0
            for i, char in enumerate(line):
                char_width = self._calculate_char_width(char, font, squeeze_halfwidth)
                line_width += char_width
                # 添加字间距（最后一个字符不添加）
                if i < len(line) - 1:
                    line_width += letter_spacing
            max_line_width = max(max_line_width, line_width)

        # 计算总高度
        line_height = temp_painter.fontMetrics().height()
        total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)

        temp_painter.end()

        return (max_line_width, total_height)
