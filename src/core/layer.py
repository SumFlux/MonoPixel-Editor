"""图层数据模型"""
import numpy as np
from typing import Tuple, Optional
from .text_object import TextObject


class Layer:
    """单个图层类"""

    def __init__(self, width: int, height: int, name: str = "Layer", layer_type: str = "bitmap"):
        """
        初始化图层

        Args:
            width: 图层宽度
            height: 图层高度
            name: 图层名称
            layer_type: 图层类型 ('bitmap' | 'text')
        """
        self.name = name
        self.width = width
        self.height = height
        self.layer_type = layer_type
        self.data = np.zeros((height, width), dtype=bool) if layer_type == "bitmap" else None
        self.text_object: Optional[TextObject] = None
        self.visible = True
        self.locked = False

    def set_pixel(self, x: int, y: int, value: bool) -> None:
        """
        设置像素值

        Args:
            x: X 坐标
            y: Y 坐标
            value: 像素值（True=黑色, False=白色）
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y, x] = value

    def get_pixel(self, x: int, y: int) -> bool:
        """
        获取像素值

        Args:
            x: X 坐标
            y: Y 坐标

        Returns:
            像素值（True=黑色, False=白色）
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return bool(self.data[y, x])
        return False

    def clear(self) -> None:
        """清空图层"""
        self.data.fill(False)

    def copy(self) -> 'Layer':
        """
        复制图层

        Returns:
            新的图层对象
        """
        new_layer = Layer(self.width, self.height, f"{self.name} Copy", self.layer_type)

        if self.layer_type == "bitmap":
            new_layer.data = self.data.copy()
        elif self.layer_type == "text" and self.text_object:
            new_layer.text_object = self.text_object.copy()

        new_layer.visible = self.visible
        new_layer.locked = self.locked
        return new_layer

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """
        获取图层内容的边界框

        Returns:
            (min_x, min_y, max_x, max_y) 如果图层为空则返回 (0, 0, 0, 0)
        """
        if not self.data.any():
            return (0, 0, 0, 0)

        rows = np.any(self.data, axis=1)
        cols = np.any(self.data, axis=0)

        min_y, max_y = np.where(rows)[0][[0, -1]]
        min_x, max_x = np.where(cols)[0][[0, -1]]

        return (min_x, min_y, max_x + 1, max_y + 1)
