"""工具基类"""
from abc import ABC, abstractmethod
from typing import Optional
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QCursor
import numpy as np

from ..core.canvas import Canvas


class BaseTool(ABC):
    """绘图工具抽象基类"""

    def __init__(self, canvas: Canvas):
        """
        初始化工具

        Args:
            canvas: 画布对象
        """
        self.canvas = canvas
        self.is_drawing = False
        self.start_pos: Optional[tuple[int, int]] = None
        self.last_pos: Optional[tuple[int, int]] = None
        self.old_layer_data: Optional[np.ndarray] = None

    def begin_draw(self) -> None:
        """开始绘制（保存当前图层状态）"""
        layer = self.canvas.get_active_layer()
        if layer:
            self.old_layer_data = layer.data.copy()

    def end_draw(self) -> Optional[tuple[np.ndarray, np.ndarray]]:
        """
        结束绘制（返回旧数据和新数据用于撤销/重做）

        Returns:
            (old_data, new_data) 或 None
        """
        layer = self.canvas.get_active_layer()
        if layer and self.old_layer_data is not None:
            new_data = layer.data.copy()
            old_data = self.old_layer_data
            self.old_layer_data = None
            return (old_data, new_data)
        return None

    @abstractmethod
    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标按下事件

        Args:
            x, y: 画布坐标
            modifiers: 键盘修饰键
        """
        pass

    @abstractmethod
    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标拖拽事件

        Args:
            x, y: 画布坐标
            modifiers: 键盘修饰键
        """
        pass

    @abstractmethod
    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """
        鼠标释放事件

        Args:
            x, y: 画布坐标
            modifiers: 键盘修饰键
        """
        pass

    def on_key_press(self, key: Qt.Key) -> None:
        """
        键盘按下事件

        Args:
            key: 按键
        """
        pass

    def get_cursor(self) -> QCursor:
        """
        获取工具光标

        Returns:
            光标对象
        """
        return QCursor(Qt.CursorShape.CrossCursor)

    def get_preview_points(self) -> list[tuple[int, int]]:
        """
        获取预览点（用于实时预览）

        Returns:
            预览点坐标列表
        """
        return []

    def reset(self) -> None:
        """重置工具状态"""
        self.is_drawing = False
        self.start_pos = None
        self.last_pos = None
        self.old_layer_data = None
