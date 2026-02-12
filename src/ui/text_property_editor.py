"""文本属性编辑器组件"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QPushButton, QComboBox, QGroupBox, QFormLayout, QTextEdit
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
import os


class TextPropertyEditor(QWidget):
    """文本属性编辑器"""

    text_changed = pyqtSignal(str)  # 文本内容改变
    font_changed = pyqtSignal(str, int)  # 字体和字号改变 (font_name, font_size)
    spacing_changed = pyqtSignal(int, int)  # 字间距和行间距改变 (letter_spacing, line_spacing)
    max_width_changed = pyqtSignal(int)  # 最大宽度改变
    position_changed = pyqtSignal(int, int)  # 位置改变 (x, y)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        self.custom_font_path = None

    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        # 设置左右边距一致，减小边距以节省空间
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(5)

        # 文本内容组
        self._create_text_group(layout)

        # 字体组
        self._create_font_group(layout)

        # 间距组
        self._create_spacing_group(layout)

        # 位置组
        self._create_position_group(layout)

    def _create_text_group(self, parent_layout: QVBoxLayout):
        """创建文本内容组"""
        group = QGroupBox("文本内容")
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setMaximumHeight(80)
        self.text_edit.setPlaceholderText("输入文本...")
        layout.addWidget(self.text_edit)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _create_font_group(self, parent_layout: QVBoxLayout):
        """创建字体组"""
        group = QGroupBox("字体")
        layout = QFormLayout()

        # 字体选择
        font_row = QHBoxLayout()
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Courier New", "Times New Roman"])
        font_row.addWidget(self.font_combo)

        self.load_font_btn = QPushButton("加载...")
        self.load_font_btn.setMaximumWidth(60)
        self.load_font_btn.clicked.connect(self._on_load_font)
        font_row.addWidget(self.load_font_btn)

        layout.addRow("字体:", font_row)

        # 字号
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 128)
        self.font_size_spin.setValue(16)
        self.font_size_spin.setSuffix(" px")
        layout.addRow("字号:", self.font_size_spin)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _create_spacing_group(self, parent_layout: QVBoxLayout):
        """创建间距组"""
        group = QGroupBox("间距")
        layout = QFormLayout()

        # 最大宽度
        self.max_width_spin = QSpinBox()
        self.max_width_spin.setRange(0, 9999)
        self.max_width_spin.setValue(0)
        self.max_width_spin.setSpecialValueText("不限制")
        self.max_width_spin.setSuffix(" px")
        layout.addRow("最大宽度:", self.max_width_spin)

        # 字间距
        self.letter_spacing_spin = QSpinBox()
        self.letter_spacing_spin.setRange(0, 50)
        self.letter_spacing_spin.setValue(0)
        self.letter_spacing_spin.setSuffix(" px")
        layout.addRow("字间距:", self.letter_spacing_spin)

        # 行间距
        self.line_spacing_spin = QSpinBox()
        self.line_spacing_spin.setRange(0, 50)
        self.line_spacing_spin.setValue(0)
        self.line_spacing_spin.setSuffix(" px")
        layout.addRow("行间距:", self.line_spacing_spin)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _create_position_group(self, parent_layout: QVBoxLayout):
        """创建位置组"""
        group = QGroupBox("位置")
        layout = QFormLayout()

        # X 坐标
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-9999, 9999)
        self.x_spin.setValue(0)
        self.x_spin.setSuffix(" px")
        layout.addRow("X:", self.x_spin)

        # Y 坐标
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-9999, 9999)
        self.y_spin.setValue(0)
        self.y_spin.setSuffix(" px")
        layout.addRow("Y:", self.y_spin)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def _connect_signals(self):
        """连接信号"""
        self.text_edit.textChanged.connect(self._on_text_changed)
        self.font_combo.currentTextChanged.connect(self._on_font_changed)
        self.font_size_spin.valueChanged.connect(self._on_font_changed)
        self.max_width_spin.valueChanged.connect(self._on_max_width_changed)
        self.letter_spacing_spin.valueChanged.connect(self._on_spacing_changed)
        self.line_spacing_spin.valueChanged.connect(self._on_spacing_changed)
        self.x_spin.valueChanged.connect(self._on_position_changed)
        self.y_spin.valueChanged.connect(self._on_position_changed)

    def _on_text_changed(self):
        """文本内容改变"""
        self.text_changed.emit(self.text_edit.toPlainText())

    def _on_font_changed(self):
        """字体改变"""
        font_name = self.font_combo.currentText()
        font_size = self.font_size_spin.value()
        self.font_changed.emit(font_name, font_size)

    def _on_spacing_changed(self):
        """间距改变"""
        letter_spacing = self.letter_spacing_spin.value()
        line_spacing = self.line_spacing_spin.value()
        self.spacing_changed.emit(letter_spacing, line_spacing)

    def _on_max_width_changed(self):
        """最大宽度改变"""
        self.max_width_changed.emit(self.max_width_spin.value())

    def _on_position_changed(self):
        """位置改变"""
        x = self.x_spin.value()
        y = self.y_spin.value()
        self.position_changed.emit(x, y)

    def _on_load_font(self):
        """加载自定义字体"""
        from PyQt6.QtWidgets import QFileDialog

        # 默认打开 fonts 文件夹
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "fonts")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择字体文件",
            fonts_dir,
            "字体文件 (*.ttf *.otf)"
        )

        if file_path:
            self.custom_font_path = file_path
            font_name = os.path.basename(file_path)
            self.font_combo.addItem(font_name)
            self.font_combo.setCurrentText(font_name)

    def load_text_object(self, text_object):
        """
        加载文本对象属性

        Args:
            text_object: TextObject 实例
        """
        # 阻止信号发射，避免循环更新
        self.blockSignals(True)

        # 设置文本内容
        self.text_edit.setPlainText(text_object.text)

        # 设置字体
        if text_object.custom_font_path:
            self.custom_font_path = text_object.custom_font_path
            font_name = os.path.basename(text_object.custom_font_path)
            # 检查是否已存在
            index = self.font_combo.findText(font_name)
            if index < 0:
                self.font_combo.addItem(font_name)
            self.font_combo.setCurrentText(font_name)
        else:
            index = self.font_combo.findText(text_object.font_name)
            if index >= 0:
                self.font_combo.setCurrentIndex(index)

        self.font_size_spin.setValue(text_object.font_size)

        # 设置间距
        self.max_width_spin.setValue(text_object.max_width)
        self.letter_spacing_spin.setValue(text_object.letter_spacing)
        self.line_spacing_spin.setValue(text_object.line_spacing)

        # 设置位置
        x, y = text_object.position
        self.x_spin.setValue(x)
        self.y_spin.setValue(y)

        # 恢复信号
        self.blockSignals(False)

    def get_custom_font_path(self):
        """获取自定义字体路径"""
        return self.custom_font_path
