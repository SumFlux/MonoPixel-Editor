"""文本工具"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QComboBox
from .base_tool import BaseTool
from ..services.text_service import TextService
from ..services.font_manager import FontManager
from ..core.text_object import TextObject
import numpy as np
import os


class TextInputDialog(QDialog):
    """文本输入对话框"""

    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("输入文本")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # 文本输入
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("文本:"))
        self.text_edit = QLineEdit()
        text_layout.addWidget(self.text_edit)
        layout.addLayout(text_layout)

        # 字体选择
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Courier New", "Times New Roman"])
        font_layout.addWidget(self.font_combo)

        # 加载字体按钮
        self.load_font_btn = QPushButton("加载字体...")
        self.load_font_btn.clicked.connect(self.load_custom_font)
        font_layout.addWidget(self.load_font_btn)
        layout.addLayout(font_layout)

        # 字号输入（像素）
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("字号(像素):"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 128)
        self.size_spin.setValue(16)
        size_layout.addWidget(self.size_spin)
        layout.addLayout(size_layout)

        # 最大宽度输入
        max_width_layout = QHBoxLayout()
        max_width_layout.addWidget(QLabel("最大宽度:"))
        self.max_width_spin = QSpinBox()
        self.max_width_spin.setRange(0, 9999)
        self.max_width_spin.setValue(0)
        self.max_width_spin.setSpecialValueText("不限制")
        max_width_layout.addWidget(self.max_width_spin)
        max_width_layout.addWidget(QLabel("像素"))
        layout.addLayout(max_width_layout)

        # 字间距输入
        letter_spacing_layout = QHBoxLayout()
        letter_spacing_layout.addWidget(QLabel("字间距:"))
        self.letter_spacing_spin = QSpinBox()
        self.letter_spacing_spin.setRange(0, 50)
        self.letter_spacing_spin.setValue(0)
        letter_spacing_layout.addWidget(self.letter_spacing_spin)
        letter_spacing_layout.addWidget(QLabel("像素"))
        layout.addLayout(letter_spacing_layout)

        # 行间距输入
        line_spacing_layout = QHBoxLayout()
        line_spacing_layout.addWidget(QLabel("行间距:"))
        self.line_spacing_spin = QSpinBox()
        self.line_spacing_spin.setRange(0, 50)
        self.line_spacing_spin.setValue(0)
        line_spacing_layout.addWidget(self.line_spacing_spin)
        line_spacing_layout.addWidget(QLabel("像素"))
        layout.addLayout(line_spacing_layout)

        # 按钮
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.custom_font_path = None

        # 加载上次的配置
        if self.config:
            self._load_config()

    def load_custom_font(self):
        """加载自定义字体"""
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

    def _load_config(self):
        """加载配置"""
        last_font = self.config.get_last_font_name()
        last_size = self.config.get_last_font_size()
        last_custom_path = self.config.get_last_custom_font_path()
        last_max_width = self.config.get_last_max_width()
        last_letter_spacing = self.config.get_last_letter_spacing()
        last_line_spacing = self.config.get_last_line_spacing()

        # 设置字号
        self.size_spin.setValue(last_size)

        # 设置最大宽度、字间距、行间距
        self.max_width_spin.setValue(last_max_width)
        self.letter_spacing_spin.setValue(last_letter_spacing)
        self.line_spacing_spin.setValue(last_line_spacing)

        # 如果有自定义字体路径，加载它
        if last_custom_path and os.path.exists(last_custom_path):
            self.custom_font_path = last_custom_path
            font_name = os.path.basename(last_custom_path)
            self.font_combo.addItem(font_name)
            self.font_combo.setCurrentText(font_name)
        else:
            # 否则设置为上次的系统字体
            index = self.font_combo.findText(last_font)
            if index >= 0:
                self.font_combo.setCurrentIndex(index)

    def accept(self):
        """保存配置并关闭对话框"""
        if self.config:
            self.config.set_last_font_name(self.font_combo.currentText())
            self.config.set_last_font_size(self.size_spin.value())
            self.config.set_last_max_width(self.max_width_spin.value())
            self.config.set_last_letter_spacing(self.letter_spacing_spin.value())
            self.config.set_last_line_spacing(self.line_spacing_spin.value())
            if self.custom_font_path:
                self.config.set_last_custom_font_path(self.custom_font_path)
        super().accept()

    def get_values(self):
        """获取输入值"""
        return {
            'text': self.text_edit.text(),
            'font_name': self.font_combo.currentText(),
            'font_size': self.size_spin.value(),
            'custom_font_path': self.custom_font_path,
            'max_width': self.max_width_spin.value(),
            'letter_spacing': self.letter_spacing_spin.value(),
            'line_spacing': self.line_spacing_spin.value()
        }


class TextTool(BaseTool):
    """文本工具"""

    def __init__(self, canvas, config=None, layer_panel=None):
        """
        初始化文本工具

        Args:
            canvas: 画布对象
            config: 配置管理器
            layer_panel: 图层面板（用于刷新）
        """
        super().__init__(canvas)
        self.config = config
        self.layer_panel = layer_panel
        self.font_manager = FontManager()
        self.text_service = TextService(self.font_manager)
        self.current_font = QFont("Arial", 16)
        self.current_font.setPixelSize(16)  # 使用像素大小
        self.squeeze_halfwidth = True
        self.text_preview = None
        self.preview_pos = None
        self.is_editing = False
        self.current_text = ""
        self.drag_offset = (0, 0)

    def on_press(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标按下"""
        # 如果已经有文本在编辑
        if self.is_editing and self.text_preview is not None:
            # 检查是否点击在文本区域内
            if self._is_point_in_text(x, y):
                # 点击在文本内，准备拖拽
                self.is_drawing = True
                px, py = self.preview_pos
                self.drag_offset = (x - px, y - py)
            else:
                # 点击在文本外，完成当前文本编辑
                self.reset()
                # 不立即开始新的文本输入，等待下次点击
        else:
            # 开始新的文本输入
            self._start_new_text(x, y)

    def on_double_click(self, x: int, y: int) -> None:
        """鼠标双击事件"""
        # 如果双击在文本区域内，进入编辑模式
        if self.is_editing and self.text_preview is not None:
            if self._is_point_in_text(x, y):
                self._edit_text()

    def _start_new_text(self, x: int, y: int) -> None:
        """开始新的文本输入"""
        self.begin_draw()

        # 显示文本输入对话框
        dialog = TextInputDialog(None, self.config)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            text = values['text']

            if not text:
                self.reset()
                return

            # 设置字体
            font_name = values['font_name']
            font_size = values['font_size']
            max_width = values['max_width']
            letter_spacing = values['letter_spacing']
            line_spacing = values['line_spacing']

            # 如果是自定义字体，加载它
            custom_font_path = values['custom_font_path'] if values['custom_font_path'] else ""
            if custom_font_path:
                loaded_font = self.font_manager.load_custom_font(custom_font_path)
                if loaded_font:
                    font_name = loaded_font

            # 创建文本对象
            text_object = TextObject(
                text=text,
                font_name=font_name,
                font_size=font_size,
                position=(x, y),
                max_width=max_width,
                letter_spacing=letter_spacing,
                line_spacing=line_spacing,
                custom_font_path=custom_font_path
            )

            # 创建文本图层
            text_layer = self.canvas.add_text_layer(text_object)

            # 刷新图层面板
            if self.layer_panel:
                self.layer_panel.refresh_layers()

            # 渲染文本预览（用于显示）
            try:
                self.current_font = QFont(font_name)
                self.current_font.setPixelSize(font_size)
                self.current_text = text

                text_bitmap = self.text_service.render_text(
                    text,
                    self.current_font,
                    self.squeeze_halfwidth,
                    max_width,
                    letter_spacing,
                    line_spacing
                )

                # 保存预览（用于显示边框）
                self.text_preview = text_bitmap
                self.preview_pos = (x, y)
                self.is_editing = True
                self.is_drawing = False

            except Exception as e:
                print(f"文本渲染失败: {e}")
                # 删除刚创建的图层
                self.canvas.remove_layer(len(self.canvas.layers) - 1)
                self.reset()
        else:
            self.reset()

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽（移动文本位置）"""
        if self.is_editing and self.text_preview is not None and self.is_drawing:
            # 使用拖拽偏移量
            new_x = x - self.drag_offset[0]
            new_y = y - self.drag_offset[1]
            self.preview_pos = (new_x, new_y)

            # 更新文本对象的位置
            layer = self.canvas.get_active_layer()
            if layer and layer.layer_type == "text" and layer.text_object:
                layer.text_object.position = (new_x, new_y)

    def on_release(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标释放"""
        self.is_drawing = False

    def on_key_press(self, key: Qt.Key) -> None:
        """键盘按下事件"""
        # 按 Enter 键可以重新编辑文本
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            if self.is_editing and self.text_preview is not None:
                self._edit_text()

    def _edit_text(self) -> None:
        """重新编辑文本"""
        if not self.is_editing:
            return

        # 显示文本输入对话框
        dialog = TextInputDialog(None, self.config)
        dialog.text_edit.setText(self.current_text)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            text = values['text']

            if not text:
                return

            # 更新字体和参数
            font_name = values['font_name']
            font_size = values['font_size']
            max_width = values['max_width']
            letter_spacing = values['letter_spacing']
            line_spacing = values['line_spacing']
            custom_font_path = values['custom_font_path'] if values['custom_font_path'] else ""

            if custom_font_path:
                loaded_font = self.font_manager.load_custom_font(custom_font_path)
                if loaded_font:
                    font_name = loaded_font

            self.current_font = QFont(font_name)
            self.current_font.setPixelSize(font_size)
            self.current_text = text

            # 更新文本对象
            layer = self.canvas.get_active_layer()
            if layer and layer.layer_type == "text" and layer.text_object:
                layer.text_object.text = text
                layer.text_object.font_name = font_name
                layer.text_object.font_size = font_size
                layer.text_object.max_width = max_width
                layer.text_object.letter_spacing = letter_spacing
                layer.text_object.line_spacing = line_spacing
                layer.text_object.custom_font_path = custom_font_path

            # 重新渲染预览
            try:
                text_bitmap = self.text_service.render_text(
                    text,
                    self.current_font,
                    self.squeeze_halfwidth,
                    max_width,
                    letter_spacing,
                    line_spacing
                )
                self.text_preview = text_bitmap
            except Exception as e:
                print(f"文本渲染失败: {e}")

    def _is_point_in_text(self, x: int, y: int) -> bool:
        """检查点是否在文本区域内"""
        if self.text_preview is None or self.preview_pos is None:
            return False

        px, py = self.preview_pos
        height, width = self.text_preview.shape

        return px <= x < px + width and py <= y < py + height

    def _rasterize_text(self) -> None:
        """栅格化文本到图层"""
        if self.text_preview is None or self.preview_pos is None:
            return

        layer = self.canvas.get_active_layer()
        if layer is None or layer.locked:
            return

        px, py = self.preview_pos
        height, width = self.text_preview.shape

        for dy in range(height):
            for dx in range(width):
                if self.text_preview[dy, dx]:
                    layer.set_pixel(px + dx, py + dy, True)

    def get_preview_points(self) -> list[tuple[int, int]]:
        """获取预览点"""
        if self.text_preview is None or self.preview_pos is None:
            return []

        points = []
        px, py = self.preview_pos
        height, width = self.text_preview.shape

        for dy in range(height):
            for dx in range(width):
                if self.text_preview[dy, dx]:
                    points.append((px + dx, py + dy))

        return points

    def draw_overlay(self, painter: QPainter, scale: float) -> None:
        """
        绘制覆盖层（文本预览边框）

        Args:
            painter: QPainter 对象
            scale: 缩放比例
        """
        if self.is_editing and self.text_preview is not None and self.preview_pos is not None:
            # 绘制蓝色虚线边框
            px, py = self.preview_pos
            height, width = self.text_preview.shape

            painter.save()

            # 设置固定宽度的边框（2px，使用 cosmetic pen）
            pen = QPen(QColor(0, 120, 215), 2, Qt.PenStyle.DashLine)  # 蓝色虚线，2px宽
            pen.setCosmetic(True)  # 固定宽度，不随缩放变化
            painter.setPen(pen)
            painter.drawRect(px, py, width, height)

            painter.restore()

    def reset(self) -> None:
        """重置工具状态"""
        super().reset()
        self.text_preview = None
        self.preview_pos = None
        self.is_editing = False
        self.current_text = ""
        self.drag_offset = (0, 0)

    def finalize(self) -> None:
        """完成文本编辑（切换工具时调用）"""
        # 文本对象已经保存在图层中，不需要栅格化
        self.reset()

    def on_layer_changed(self) -> None:
        """图层切换时调用，清除预览状态"""
        # 如果当前有文本预览，清除它
        if self.is_editing:
            self.reset()

    def set_squeeze_halfwidth(self, squeeze: bool) -> None:
        """
        设置是否挤压半角字符

        Args:
            squeeze: 是否挤压
        """
        self.squeeze_halfwidth = squeeze
