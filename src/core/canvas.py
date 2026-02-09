"""画布数据模型"""
import numpy as np
from typing import List, Optional
from .layer import Layer


class Canvas:
    """画布类，管理多个图层"""

    def __init__(self, width: int, height: int):
        """
        初始化画布

        Args:
            width: 画布宽度
            height: 画布高度
        """
        self.width = width
        self.height = height
        self.layers: List[Layer] = []
        self.active_layer_index = 0
        self.grid_visible = True

        # 创建默认图层
        self.add_layer("Background")

    def add_layer(self, name: Optional[str] = None) -> Layer:
        """
        添加新图层

        Args:
            name: 图层名称，如果为 None 则自动生成

        Returns:
            新创建的图层
        """
        if name is None:
            name = f"Layer {len(self.layers) + 1}"

        layer = Layer(self.width, self.height, name)
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1
        return layer

    def remove_layer(self, index: int) -> bool:
        """
        删除图层

        Args:
            index: 图层索引

        Returns:
            是否成功删除
        """
        if len(self.layers) <= 1:
            return False

        if 0 <= index < len(self.layers):
            self.layers.pop(index)

            # 调整活动图层索引
            if self.active_layer_index >= len(self.layers):
                self.active_layer_index = len(self.layers) - 1

            return True

        return False

    def move_layer(self, from_index: int, to_index: int) -> bool:
        """
        移动图层

        Args:
            from_index: 源索引
            to_index: 目标索引

        Returns:
            是否成功移动
        """
        if (0 <= from_index < len(self.layers) and
            0 <= to_index < len(self.layers) and
            from_index != to_index):

            layer = self.layers.pop(from_index)
            self.layers.insert(to_index, layer)

            # 更新活动图层索引
            if self.active_layer_index == from_index:
                # 移动的是活动图层
                self.active_layer_index = to_index
            elif from_index < to_index:
                # 向后移动，中间的图层索引减1
                if from_index < self.active_layer_index <= to_index:
                    self.active_layer_index -= 1
            else:
                # 向前移动，中间的图层索引加1
                if to_index <= self.active_layer_index < from_index:
                    self.active_layer_index += 1

            return True

        return False

    def get_active_layer(self) -> Optional[Layer]:
        """
        获取当前活动图层

        Returns:
            活动图层，如果没有则返回 None
        """
        if 0 <= self.active_layer_index < len(self.layers):
            return self.layers[self.active_layer_index]
        return None

    def merge_visible_layers(self) -> np.ndarray:
        """
        合并所有可见图层

        Returns:
            合并后的位图数据
        """
        result = np.zeros((self.height, self.width), dtype=bool)

        # 从下到上依次叠加
        for layer in self.layers:
            if layer.visible:
                # 黑色像素（True）遮挡下层，白色像素（False）透明
                result = np.logical_or(result, layer.data)

        return result

    def resize(self, new_width: int, new_height: int) -> None:
        """
        调整画布大小

        Args:
            new_width: 新宽度
            new_height: 新高度
        """
        self.width = new_width
        self.height = new_height

        # 调整所有图层大小
        for layer in self.layers:
            old_data = layer.data
            layer.data = np.zeros((new_height, new_width), dtype=bool)
            layer.width = new_width
            layer.height = new_height

            # 复制旧数据（左上角对齐）
            copy_height = min(old_data.shape[0], new_height)
            copy_width = min(old_data.shape[1], new_width)
            layer.data[:copy_height, :copy_width] = old_data[:copy_height, :copy_width]
