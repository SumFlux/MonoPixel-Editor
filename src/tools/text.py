"""文本工具"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QComboBox
from .base_tool import BaseTool
from ..services.text_service import TextService
from ..services.font_manager import FontManager
import numpy as np
import os


class TextInputDialog(QDialog):
    """文本输入对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
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

    def get_values(self):
        """获取输入值"""
        return {
            'text': self.text_edit.text(),
            'font_name': self.font_combo.currentText(),
            'font_size': self.size_spin.value(),
            'custom_font_path': self.custom_font_path
        }


class TextTool(BaseTool):
    """文本工具"""

    def __init__(self, canvas):
        """
        初始化文本工具

        Args:
            canvas: 画布对象
        """
        super().__init__(canvas)
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
                # 点击在文本外，先栅格化当前文本并取消选择
                self._rasterize_text()
                self.reset()
                # 不立即开始新的文本输入，等待下次点击
        else:
            # 开始新的文本输入
            self._start_new_text(x, y)

    def _start_new_text(self, x: int, y: int) -> None:
        """开始新的文本输入"""
        self.begin_draw()

        # 显示文本输入对话框
        dialog = TextInputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            text = values['text']

            if not text:
                self.reset()
                return

            # 设置字体
            font_name = values['font_name']
            font_size = values['font_size']

            # 如果是自定义字体，加载它
            if values['custom_font_path']:
                loaded_font = self.font_manager.load_custom_font(values['custom_font_path'])
                if loaded_font:
                    font_name = loaded_font

            # 创建字体对象，使用像素大小
            self.current_font = QFont(font_name)
            self.current_font.setPixelSize(font_size)
            self.current_text = text

            # 渲染文本
            try:
                text_bitmap = self.text_service.render_text(
                    text, self.current_font, self.squeeze_halfwidth
                )

                # 保存预览
                self.text_preview = text_bitmap
                self.preview_pos = (x, y)
                self.is_editing = True
                self.is_drawing = False

            except Exception as e:
                print(f"文本渲染失败: {e}")
                self.reset()
        else:
            self.reset()

    def on_drag(self, x: int, y: int, modifiers: Qt.KeyboardModifier) -> None:
        """鼠标拖拽（移动文本位置）"""
        if self.is_editing and self.text_preview is not None and self.is_drawing:
            # 使用拖拽偏移量
            self.preview_pos = (x - self.drag_offset[0], y - self.drag_offset[1])

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
        dialog = TextInputDialog()
        dialog.text_edit.setText(self.current_text)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            text = values['text']

            if not text:
                return

            # 更新字体
            font_name = values['font_name']
            font_size = values['font_size']

            if values['custom_font_path']:
                loaded_font = self.font_manager.load_custom_font(values['custom_font_path'])
                if loaded_font:
                    font_name = loaded_font

            self.current_font = QFont(font_name)
            self.current_font.setPixelSize(font_size)
            self.current_text = text

            # 重新渲染
            try:
                text_bitmap = self.text_service.render_text(
                    text, self.current_font, self.squeeze_halfwidth
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
        if self.is_editing and self.text_preview is not None:
            self._rasterize_text()
        self.reset()

    def set_squeeze_halfwidth(self, squeeze: bool) -> None:
        """
        设置是否挤压半角字符

        Args:
            squeeze: 是否挤压
        """
        self.squeeze_halfwidth = squeeze
