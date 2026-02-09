"""图层面板组件"""
from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from ..core.canvas import Canvas


class LayerPanel(QDockWidget):
    """图层面板类"""

    layer_changed = pyqtSignal()  # 图层改变信号
    active_layer_changed = pyqtSignal(int)  # 活动图层改变信号

    def __init__(self, canvas: Canvas):
        """
        初始化图层面板

        Args:
            canvas: 画布对象
        """
        super().__init__("图层")
        self.canvas = canvas
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # 创建主部件
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # 图层列表
        self.layer_list = QListWidget()
        self.layer_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.layer_list.currentRowChanged.connect(self._on_layer_selected)
        layout.addWidget(self.layer_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 新建图层按钮
        self.add_button = QPushButton("新建")
        self.add_button.clicked.connect(self._on_add_layer)
        button_layout.addWidget(self.add_button)

        # 删除图层按钮
        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self._on_delete_layer)
        button_layout.addWidget(self.delete_button)

        # 复制图层按钮
        self.copy_button = QPushButton("复制")
        self.copy_button.clicked.connect(self._on_copy_layer)
        button_layout.addWidget(self.copy_button)

        layout.addLayout(button_layout)

        # 上移/下移按钮
        move_layout = QHBoxLayout()

        self.move_up_button = QPushButton("上移")
        self.move_up_button.clicked.connect(self._on_move_up)
        move_layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("下移")
        self.move_down_button.clicked.connect(self._on_move_down)
        move_layout.addWidget(self.move_down_button)

        layout.addLayout(move_layout)

        self.setWidget(main_widget)

        # 初始化图层列表
        self.refresh_layers()

    def refresh_layers(self) -> None:
        """刷新图层列表"""
        self.layer_list.clear()

        # 从上到下显示图层（索引从大到小）
        for i in range(len(self.canvas.layers) - 1, -1, -1):
            layer = self.canvas.layers[i]
            item = QListWidgetItem()

            # 图层名称
            name = layer.name
            if not layer.visible:
                name += " (隐藏)"
            if layer.locked:
                name += " 🔒"

            item.setText(name)
            item.setData(Qt.ItemDataRole.UserRole, i)  # 存储图层索引

            self.layer_list.addItem(item)

        # 选中活动图层
        active_index = self.canvas.active_layer_index
        list_index = len(self.canvas.layers) - 1 - active_index
        self.layer_list.setCurrentRow(list_index)

    def _on_layer_selected(self, list_index: int) -> None:
        """
        图层选择事件

        Args:
            list_index: 列表索引
        """
        if list_index >= 0:
            # 转换为图层索引（反向）
            layer_index = len(self.canvas.layers) - 1 - list_index
            self.canvas.active_layer_index = layer_index
            self.active_layer_changed.emit(layer_index)

    def _on_add_layer(self) -> None:
        """新建图层"""
        name, ok = QInputDialog.getText(self, "新建图层", "图层名称:")
        if ok and name:
            self.canvas.add_layer(name)
            self.refresh_layers()
            self.layer_changed.emit()

    def _on_delete_layer(self) -> None:
        """删除图层"""
        if len(self.canvas.layers) <= 1:
            QMessageBox.warning(self, "警告", "至少需要保留一个图层！")
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除图层 '{self.canvas.get_active_layer().name}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.canvas.remove_layer(self.canvas.active_layer_index)
            self.refresh_layers()
            self.layer_changed.emit()

    def _on_copy_layer(self) -> None:
        """复制图层"""
        active_layer = self.canvas.get_active_layer()
        if active_layer:
            copied_layer = active_layer.copy()
            self.canvas.layers.append(copied_layer)
            self.canvas.active_layer_index = len(self.canvas.layers) - 1
            self.refresh_layers()
            self.layer_changed.emit()

    def _on_move_up(self) -> None:
        """上移图层"""
        current_index = self.canvas.active_layer_index
        if current_index < len(self.canvas.layers) - 1:
            self.canvas.move_layer(current_index, current_index + 1)
            self.refresh_layers()
            self.layer_changed.emit()

    def _on_move_down(self) -> None:
        """下移图层"""
        current_index = self.canvas.active_layer_index
        if current_index > 0:
            self.canvas.move_layer(current_index, current_index - 1)
            self.refresh_layers()
            self.layer_changed.emit()

    def toggle_layer_visibility(self) -> None:
        """切换图层可见性"""
        layer = self.canvas.get_active_layer()
        if layer:
            layer.visible = not layer.visible
            self.refresh_layers()
            self.layer_changed.emit()

    def toggle_layer_lock(self) -> None:
        """切换图层锁定"""
        layer = self.canvas.get_active_layer()
        if layer:
            layer.locked = not layer.locked
            self.refresh_layers()
            self.layer_changed.emit()

    def rename_layer(self) -> None:
        """重命名图层"""
        layer = self.canvas.get_active_layer()
        if layer:
            name, ok = QInputDialog.getText(
                self, "重命名图层",
                "新名称:",
                text=layer.name
            )
            if ok and name:
                layer.name = name
                self.refresh_layers()
                self.layer_changed.emit()
