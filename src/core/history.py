"""撤销/重做历史管理"""
from typing import List, Optional
from abc import ABC, abstractmethod
import numpy as np


class Command(ABC):
    """命令抽象基类"""

    @abstractmethod
    def execute(self) -> None:
        """执行命令"""
        pass

    @abstractmethod
    def undo(self) -> None:
        """撤销命令"""
        pass


class DrawCommand(Command):
    """绘图命令"""

    def __init__(self, layer, old_data: np.ndarray, new_data: np.ndarray):
        """
        初始化绘图命令

        Args:
            layer: 图层对象
            old_data: 旧的图层数据
            new_data: 新的图层数据
        """
        self.layer = layer
        self.old_data = old_data.copy()
        self.new_data = new_data.copy()

    def execute(self) -> None:
        """执行命令"""
        self.layer.data = self.new_data.copy()

    def undo(self) -> None:
        """撤销命令"""
        self.layer.data = self.old_data.copy()


class AddLayerCommand(Command):
    """添加图层命令"""

    def __init__(self, canvas, layer_name: str):
        """
        初始化添加图层命令

        Args:
            canvas: 画布对象
            layer_name: 图层名称
        """
        self.canvas = canvas
        self.layer_name = layer_name
        self.layer = None
        self.layer_index = None

    def execute(self) -> None:
        """执行命令"""
        self.layer = self.canvas.add_layer(self.layer_name)
        self.layer_index = len(self.canvas.layers) - 1

    def undo(self) -> None:
        """撤销命令"""
        if self.layer_index is not None:
            self.canvas.remove_layer(self.layer_index)


class RemoveLayerCommand(Command):
    """删除图层命令"""

    def __init__(self, canvas, layer_index: int):
        """
        初始化删除图层命令

        Args:
            canvas: 画布对象
            layer_index: 图层索引
        """
        self.canvas = canvas
        self.layer_index = layer_index
        self.layer = None
        self.old_active_index = None

    def execute(self) -> None:
        """执行命令"""
        if 0 <= self.layer_index < len(self.canvas.layers):
            # 保存图层（不使用 copy，直接保存引用）
            self.layer = self.canvas.layers[self.layer_index]
            self.old_active_index = self.canvas.active_layer_index
            self.canvas.remove_layer(self.layer_index)

    def undo(self) -> None:
        """撤销命令"""
        if self.layer is not None:
            self.canvas.layers.insert(self.layer_index, self.layer)
            self.canvas.active_layer_index = self.old_active_index


class MoveLayerCommand(Command):
    """移动图层命令"""

    def __init__(self, canvas, from_index: int, to_index: int):
        """
        初始化移动图层命令

        Args:
            canvas: 画布对象
            from_index: 源索引
            to_index: 目标索引
        """
        self.canvas = canvas
        self.from_index = from_index
        self.to_index = to_index

    def execute(self) -> None:
        """执行命令"""
        self.canvas.move_layer(self.from_index, self.to_index)

    def undo(self) -> None:
        """撤销命令"""
        self.canvas.move_layer(self.to_index, self.from_index)


class History:
    """历史记录管理器"""

    def __init__(self, max_size: int = 50):
        """
        初始化历史记录

        Args:
            max_size: 最大历史记录数
        """
        self.max_size = max_size
        self.commands: List[Command] = []
        self.current_index = -1

    def execute(self, command: Command) -> None:
        """
        执行命令并添加到历史记录

        Args:
            command: 命令对象
        """
        # 执行命令
        command.execute()

        # 清除当前位置之后的所有命令
        self.commands = self.commands[:self.current_index + 1]

        # 添加新命令
        self.commands.append(command)
        self.current_index += 1

        # 限制历史记录大小
        if len(self.commands) > self.max_size:
            self.commands.pop(0)
            self.current_index -= 1

    def undo(self) -> bool:
        """
        撤销上一个命令

        Returns:
            是否成功撤销
        """
        if self.can_undo():
            self.commands[self.current_index].undo()
            self.current_index -= 1
            return True
        return False

    def redo(self) -> bool:
        """
        重做下一个命令

        Returns:
            是否成功重做
        """
        if self.can_redo():
            self.current_index += 1
            self.commands[self.current_index].execute()
            return True
        return False

    def can_undo(self) -> bool:
        """
        是否可以撤销

        Returns:
            是否可以撤销
        """
        return self.current_index >= 0

    def can_redo(self) -> bool:
        """
        是否可以重做

        Returns:
            是否可以重做
        """
        return self.current_index < len(self.commands) - 1

    def clear(self) -> None:
        """清空历史记录"""
        self.commands.clear()
        self.current_index = -1
