"""选择工具"""
import numpy as np
from typing import Optional, Tuple
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QPainter, QPen, QColor
from .base_tool import BaseTool
from ..core.canvas import Canvas


class SelectTool(BaseTool):
    """选择工具类"""

    def __init__(self, canvas: Canvas):
        """
        初始化选择工具

        Args:
            canvas: 画布对象
        """
        super().__init__(canvas)
        self.selection_rect: Optional[Tuple[int, int, int, int]] = None  # (x, y, width, height)
        self.selected_data: Optional[np.ndarray] = None
        self.is_moving = False
        self.is_resizing = False
        self.resize_handle: Optional[str] = None  # 'nw', 'ne', 'sw', 'se', 'n', 's', 'e', 'w'
        self.move_start_pos: Optional[Tuple[int, int]] = None
        self.original_rect: Optional[Tuple[int, int, int, int]] = None
        self.drag_start_pos: Optional[Tuple[int, int]] = None

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标按下事件

        Args:
            x: X 坐标
            y: Y 坐标
            modifiers: 键盘修饰键
        """
        self.is_drawing = True

        # 检查是否点击在选区内或手柄上
        if self.selection_rect:
            handle = self._get_handle_at_pos(x, y)
            if handle:
                # 点击在手柄上，开始缩放
                self.begin_draw()
                self.is_resizing = True
                self.resize_handle = handle
                self.move_start_pos = (x, y)
                self.original_rect = self.selection_rect
                return
            elif self._is_point_in_selection(x, y):
                # 点击在选区内，开始移动
                self.begin_draw()
                self.is_moving = True
                self.move_start_pos = (x, y)
                self.original_rect = self.selection_rect
                return

        # 开始新的选区
        self.start_pos = (x, y)
        self.drag_start_pos = (x, y)
        self.selection_rect = None
        self.selected_data = None
        self.is_moving = False
        self.is_resizing = False

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标拖拽事件

        Args:
            x: X 坐标
            y: Y 坐标
            modifiers: 键盘修饰键
        """
        if self.is_moving and self.move_start_pos and self.original_rect:
            # 移动选区
            dx = x - self.move_start_pos[0]
            dy = y - self.move_start_pos[1]
            orig_x, orig_y, width, height = self.original_rect
            self.selection_rect = (orig_x + dx, orig_y + dy, width, height)
        elif self.is_resizing and self.move_start_pos and self.original_rect and self.resize_handle:
            # 缩放选区
            self.selection_rect = self._calculate_resized_rect(x, y)
        elif self.start_pos:
            # 绘制选区
            self.drag_start_pos = (x, y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标释放事件

        Args:
            x: X 坐标
            y: Y 坐标
            modifiers: 键盘修饰键
        """
        layer = self.canvas.get_active_layer()
        if not layer:
            self.is_drawing = False
            return

        if self.is_moving:
            # 完成移动
            if self.selected_data is not None and self.selection_rect and self.original_rect:
                # 清除原始位置
                self._clear_rect(layer.data, self.original_rect)
                # 应用到新位置
                self._apply_selection_to_layer(layer.data)
            self.is_moving = False
            self.move_start_pos = None
            self.original_rect = None
        elif self.is_resizing:
            # 完成缩放
            if self.selected_data is not None and self.selection_rect and self.original_rect:
                # 缩放选区数据
                scaled_data = self._scale_selection(self.selected_data, self.selection_rect)
                # 清除原始位置
                self._clear_rect(layer.data, self.original_rect)
                # 应用缩放后的数据
                self._apply_scaled_data(layer.data, scaled_data)
                # 更新选区数据
                self.selected_data = scaled_data
            self.is_resizing = False
            self.resize_handle = None
            self.move_start_pos = None
            self.original_rect = None
        elif self.start_pos and self.drag_start_pos:
            # 完成选区绘制
            x1, y1 = self.start_pos
            x2, y2 = self.drag_start_pos

            # 确保坐标正确
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)

            width = right - left
            height = bottom - top

            if width > 0 and height > 0:
                self.selection_rect = (left, top, width, height)
                # 提取选区数据
                self.selected_data = self._extract_selection(layer.data)

            self.start_pos = None
            self.drag_start_pos = None

        self.is_drawing = False

    def get_cursor(self) -> QCursor:
        """
        获取光标

        Returns:
            光标对象
        """
        return QCursor(Qt.CursorShape.CrossCursor)

    def draw_overlay(self, painter: QPainter, scale: float) -> None:
        """
        绘制覆盖层（选区边框和手柄）

        Args:
            painter: QPainter 对象
            scale: 缩放比例
        """
        if self.start_pos and self.drag_start_pos and not self.selection_rect:
            # 绘制正在创建的选区
            x1, y1 = self.start_pos
            x2, y2 = self.drag_start_pos
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            pen = QPen(QColor(0, 120, 215), 1 / scale, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawRect(left, top, width, height)

        if self.selection_rect:
            # 绘制选区边框（固定粗细）
            x, y, width, height = self.selection_rect

            # 保存当前画笔状态
            painter.save()

            # 设置固定粗细的边框（1px，不随缩放变化）
            pen = QPen(QColor(0, 120, 215), 0, Qt.PenStyle.DashLine)  # 0 表示 1px 固定宽度
            painter.setPen(pen)
            painter.drawRect(x, y, width, height)

            # 绘制手柄（固定视图大小，使用 cosmetic 绘制）
            handle_size = 6  # 视图像素大小
            handles = self._get_handle_positions()

            # 使用 cosmetic pen 和 brush
            painter.setPen(QPen(QColor(0, 120, 215), 1))
            painter.setBrush(QColor(0, 120, 215))

            for handle_pos in handles.values():
                hx, hy = handle_pos
                # 计算手柄在场景坐标中的大小（除以缩放比例）
                half_size = handle_size / (2 * scale)
                painter.drawRect(
                    int(hx - half_size),
                    int(hy - half_size),
                    int(handle_size / scale),
                    int(handle_size / scale)
                )

            # 恢复画笔状态
            painter.restore()

    def clear_selection(self) -> None:
        """清除选区"""
        self.selection_rect = None
        self.selected_data = None
        self.start_pos = None
        self.drag_start_pos = None
        self.is_moving = False
        self.is_resizing = False

    def has_selection(self) -> bool:
        """
        是否有选区

        Returns:
            是否有选区
        """
        return self.selection_rect is not None

    def _extract_selection(self, layer_data: np.ndarray) -> np.ndarray:
        """
        提取选区数据

        Args:
            layer_data: 图层数据

        Returns:
            选区数据
        """
        if not self.selection_rect:
            return np.array([])

        x, y, width, height = self.selection_rect
        height_max, width_max = layer_data.shape

        # 裁剪到图层边界
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(width_max, x + width)
        y2 = min(height_max, y + height)

        return layer_data[y1:y2, x1:x2].copy()

    def _clear_rect(self, layer_data: np.ndarray, rect: Tuple[int, int, int, int]) -> None:
        """
        清除矩形区域

        Args:
            layer_data: 图层数据
            rect: 矩形 (x, y, width, height)
        """
        x, y, width, height = rect
        height_max, width_max = layer_data.shape

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(width_max, x + width)
        y2 = min(height_max, y + height)

        layer_data[y1:y2, x1:x2] = False

    def _apply_selection_to_layer(self, layer_data: np.ndarray) -> None:
        """
        将选区数据应用到图层

        Args:
            layer_data: 图层数据
        """
        if not self.selection_rect or self.selected_data is None:
            return

        x, y, width, height = self.selection_rect
        sel_height, sel_width = self.selected_data.shape
        height_max, width_max = layer_data.shape

        # 应用选区数据到新位置
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(width_max, x + sel_width)
        y2 = min(height_max, y + sel_height)

        # 计算实际可以复制的区域
        copy_width = x2 - x1
        copy_height = y2 - y1

        if copy_width > 0 and copy_height > 0:
            layer_data[y1:y2, x1:x2] = self.selected_data[:copy_height, :copy_width]

    def _apply_scaled_data(self, layer_data: np.ndarray, scaled_data: np.ndarray) -> None:
        """
        将缩放后的数据应用到图层

        Args:
            layer_data: 图层数据
            scaled_data: 缩放后的数据
        """
        if not self.selection_rect:
            return

        x, y, width, height = self.selection_rect
        sel_height, sel_width = scaled_data.shape
        height_max, width_max = layer_data.shape

        # 应用数据到新位置
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(width_max, x + sel_width)
        y2 = min(height_max, y + sel_height)

        # 计算实际可以复制的区域
        copy_width = x2 - x1
        copy_height = y2 - y1

        if copy_width > 0 and copy_height > 0:
            layer_data[y1:y2, x1:x2] = scaled_data[:copy_height, :copy_width]

    def _scale_selection(self, data: np.ndarray, target_rect: Tuple[int, int, int, int]) -> np.ndarray:
        """
        缩放选区数据（最近邻插值）

        Args:
            data: 原始数据
            target_rect: 目标矩形 (x, y, width, height)

        Returns:
            缩放后的数据
        """
        _, _, target_width, target_height = target_rect
        src_height, src_width = data.shape

        if target_width <= 0 or target_height <= 0:
            return data

        # 最近邻插值
        result = np.zeros((target_height, target_width), dtype=bool)

        scale_x = src_width / target_width
        scale_y = src_height / target_height

        for y in range(target_height):
            for x in range(target_width):
                src_x = int(x * scale_x)
                src_y = int(y * scale_y)
                # 确保不越界
                src_x = min(src_x, src_width - 1)
                src_y = min(src_y, src_height - 1)
                result[y, x] = data[src_y, src_x]

        return result

    def _is_point_in_selection(self, x: int, y: int) -> bool:
        """
        判断点是否在选区内

        Args:
            x: X 坐标
            y: Y 坐标

        Returns:
            是否在选区内
        """
        if not self.selection_rect:
            return False

        sel_x, sel_y, sel_width, sel_height = self.selection_rect
        return sel_x <= x < sel_x + sel_width and sel_y <= y < sel_y + sel_height

    def _get_handle_positions(self) -> dict:
        """
        获取所有手柄的位置

        Returns:
            手柄位置字典 {handle_name: (x, y)}
        """
        if not self.selection_rect:
            return {}

        x, y, width, height = self.selection_rect
        return {
            'nw': (x, y),
            'n': (x + width / 2, y),
            'ne': (x + width, y),
            'e': (x + width, y + height / 2),
            'se': (x + width, y + height),
            's': (x + width / 2, y + height),
            'sw': (x, y + height),
            'w': (x, y + height / 2),
        }

    def _get_handle_at_pos(self, x: int, y: int) -> Optional[str]:
        """
        获取指定位置的手柄

        Args:
            x: X 坐标
            y: Y 坐标

        Returns:
            手柄名称（如果有）
        """
        handles = self._get_handle_positions()
        handle_size = 6  # 手柄大小

        for name, (hx, hy) in handles.items():
            if abs(x - hx) <= handle_size and abs(y - hy) <= handle_size:
                return name

        return None

    def _calculate_resized_rect(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        计算缩放后的矩形

        Args:
            x: 当前 X 坐标
            y: 当前 Y 坐标

        Returns:
            新的矩形 (x, y, width, height)
        """
        if not self.original_rect or not self.resize_handle:
            return self.selection_rect or (0, 0, 0, 0)

        orig_x, orig_y, orig_width, orig_height = self.original_rect
        handle = self.resize_handle

        new_x = orig_x
        new_y = orig_y
        new_width = orig_width
        new_height = orig_height

        # 根据手柄位置调整矩形
        if 'n' in handle:
            new_y = y
            new_height = orig_y + orig_height - y
        if 's' in handle:
            new_height = y - orig_y
        if 'w' in handle:
            new_x = x
            new_width = orig_x + orig_width - x
        if 'e' in handle:
            new_width = x - orig_x

        # 确保宽度和高度为正
        if new_width < 0:
            new_x += new_width
            new_width = -new_width
        if new_height < 0:
            new_y += new_height
            new_height = -new_height

        # 最小尺寸
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        return (new_x, new_y, new_width, new_height)
