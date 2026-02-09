"""属性面板组件"""
from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QLabel, QSlider,
    QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..utils.constants import BRUSH_SIZES, FILL_MODE_OUTLINE, FILL_MODE_FILLED, FILL_MODE_BOTH


class PropertyPanel(QDockWidget):
    """属性面板类"""

    brush_size_changed = pyqtSignal(int)
    fill_mode_changed = pyqtSignal(str)

    def __init__(self):
        """初始化属性面板"""
        super().__init__("属性")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # 创建主部件
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # 笔触/橡皮擦大小
        self._create_brush_size_group(layout)

        # 填充模式
        self._create_fill_mode_group(layout)

        # 添加弹性空间
        layout.addStretch()

        self.setWidget(main_widget)

    def _create_brush_size_group(self, parent_layout: QVBoxLayout) -> None:
        """
        创建笔触大小组

        Args:
            parent_layout: 父布局
        """
        group = QGroupBox("笔触/橡皮擦大小")
        layout = QFormLayout()

        # 大小滑块
        self.brush_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.brush_size_slider.setMinimum(0)
        self.brush_size_slider.setMaximum(len(BRUSH_SIZES) - 1)
        self.brush_size_slider.setValue(0)  # 默认 1px
        self.brush_size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brush_size_slider.setTickInterval(1)

        # 大小标签
        self.brush_size_label = QLabel(f"{BRUSH_SIZES[0]}px")

        # 连接信号
        self.brush_size_slider.valueChanged.connect(self._on_brush_size_changed)

        layout.addRow("大小:", self.brush_size_slider)
        layout.addRow("", self.brush_size_label)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _create_fill_mode_group(self, parent_layout: QVBoxLayout) -> None:
        """
        创建填充模式组

        Args:
            parent_layout: 父布局
        """
        group = QGroupBox("填充模式")
        layout = QFormLayout()

        # 填充模式下拉框
        self.fill_mode_combo = QComboBox()
        self.fill_mode_combo.addItem("轮廓", FILL_MODE_OUTLINE)
        self.fill_mode_combo.addItem("填充", FILL_MODE_FILLED)
        self.fill_mode_combo.addItem("轮廓+填充", FILL_MODE_BOTH)

        # 连接信号
        self.fill_mode_combo.currentIndexChanged.connect(self._on_fill_mode_changed)

        layout.addRow("模式:", self.fill_mode_combo)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _on_brush_size_changed(self, index: int) -> None:
        """
        笔触大小改变事件

        Args:
            index: 滑块索引
        """
        size = BRUSH_SIZES[index]
        self.brush_size_label.setText(f"{size}px")
        self.brush_size_changed.emit(size)

    def _on_fill_mode_changed(self, index: int) -> None:
        """
        填充模式改变事件

        Args:
            index: 下拉框索引
        """
        mode = self.fill_mode_combo.itemData(index)
        self.fill_mode_changed.emit(mode)

    def get_brush_size(self) -> int:
        """
        获取当前笔触大小

        Returns:
            笔触大小
        """
        index = self.brush_size_slider.value()
        return BRUSH_SIZES[index]

    def get_fill_mode(self) -> str:
        """
        获取当前填充模式

        Returns:
            填充模式
        """
        index = self.fill_mode_combo.currentIndex()
        return self.fill_mode_combo.itemData(index)
