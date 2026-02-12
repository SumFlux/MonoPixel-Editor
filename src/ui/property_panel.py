"""属性面板组件"""
from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QLabel, QSlider,
    QComboBox, QGroupBox, QFormLayout, QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..utils.constants import BRUSH_SIZES, FILL_MODE_OUTLINE, FILL_MODE_FILLED, FILL_MODE_BOTH
from .text_property_editor import TextPropertyEditor


class PropertyPanel(QDockWidget):
    """属性面板类"""

    brush_size_changed = pyqtSignal(int)
    fill_mode_changed = pyqtSignal(str)
    text_property_changed = pyqtSignal()  # 文本属性改变信号

    def __init__(self):
        """初始化属性面板"""
        super().__init__("属性")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        # 设置最小宽度，确保内容显示完整
        self.setMinimumWidth(280)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 创建主部件
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        # 设置左右边距一致，减小边距以节省空间
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(5)

        # 使用堆叠部件切换不同的属性编辑器
        self.stacked_widget = QStackedWidget()

        # 创建通用工具属性页面
        general_page = QWidget()
        general_layout = QVBoxLayout(general_page)

        # 笔触/橡皮擦大小
        self._create_brush_size_group(general_layout)

        # 填充模式
        self._create_fill_mode_group(general_layout)

        # 添加弹性空间
        general_layout.addStretch()

        # 创建文本属性编辑器页面
        self.text_editor = TextPropertyEditor()
        self._connect_text_editor_signals()

        # 添加到堆叠部件
        self.stacked_widget.addWidget(general_page)  # 索引 0: 通用属性
        self.stacked_widget.addWidget(self.text_editor)  # 索引 1: 文本属性

        main_layout.addWidget(self.stacked_widget)

        # 将主部件放入滚动区域
        scroll_area.setWidget(main_widget)
        self.setWidget(scroll_area)

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

    def _connect_text_editor_signals(self):
        """连接文本编辑器信号"""
        self.text_editor.text_changed.connect(lambda: self.text_property_changed.emit())
        self.text_editor.font_changed.connect(lambda: self.text_property_changed.emit())
        self.text_editor.spacing_changed.connect(lambda: self.text_property_changed.emit())
        self.text_editor.max_width_changed.connect(lambda: self.text_property_changed.emit())
        self.text_editor.position_changed.connect(lambda: self.text_property_changed.emit())

    def show_general_properties(self):
        """显示通用工具属性"""
        self.stacked_widget.setCurrentIndex(0)

    def show_text_properties(self, text_object=None):
        """
        显示文本属性编辑器

        Args:
            text_object: TextObject 实例（可选）
        """
        self.stacked_widget.setCurrentIndex(1)
        if text_object:
            self.text_editor.load_text_object(text_object)

    def get_text_editor(self):
        """获取文本属性编辑器"""
        return self.text_editor
