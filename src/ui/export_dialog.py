"""导出对话框"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QGroupBox, QFormLayout,
    QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import numpy as np
from pathlib import Path

from ..core.canvas import Canvas
from ..services.export_service import ExportService
from ..services.preview_service import PreviewService


class ExportDialog(QDialog):
    """导出对话框类"""

    def __init__(self, canvas: Canvas, parent=None):
        """
        初始化导出对话框

        Args:
            canvas: 画布对象
            parent: 父窗口
        """
        super().__init__(parent)
        self.canvas = canvas
        self.setWindowTitle("导出")
        self.setModal(True)
        self.resize(800, 600)

        # 创建 UI
        self._create_ui()

        # 更新预览
        self._update_preview()

    def _create_ui(self) -> None:
        """创建 UI"""
        layout = QVBoxLayout(self)

        # 文件名输入
        file_group = QGroupBox("文件")
        file_layout = QFormLayout()

        self.filename_edit = QLineEdit("image")
        file_layout.addRow("文件名:", self.filename_edit)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # 导出设置
        settings_group = QGroupBox("导出设置")
        settings_layout = QFormLayout()

        # 扫描模式
        self.scan_mode_combo = QComboBox()
        self.scan_mode_combo.addItem("水平扫描（逐行）", "horizontal")
        self.scan_mode_combo.addItem("垂直扫描（Page mode）", "vertical")
        self.scan_mode_combo.currentIndexChanged.connect(self._update_preview)
        settings_layout.addRow("扫描模式:", self.scan_mode_combo)

        # 位序
        self.bit_order_combo = QComboBox()
        self.bit_order_combo.addItem("MSB first", True)
        self.bit_order_combo.addItem("LSB first", False)
        self.bit_order_combo.currentIndexChanged.connect(self._update_preview)
        settings_layout.addRow("位序:", self.bit_order_combo)

        # 数据格式
        self.format_combo = QComboBox()
        self.format_combo.addItem("C Array (.h)", "c_array")
        self.format_combo.addItem("Binary (.bin)", "binary")
        self.format_combo.addItem("PNG Image (.png)", "png")
        settings_layout.addRow("数据格式:", self.format_combo)

        # 反色
        self.invert_checkbox = QCheckBox("反色")
        self.invert_checkbox.stateChanged.connect(self._update_preview)
        settings_layout.addRow("", self.invert_checkbox)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # 预览区
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout()

        self.preview_view = QGraphicsView()
        self.preview_scene = QGraphicsScene()
        self.preview_view.setScene(self.preview_scene)
        self.preview_view.setMinimumHeight(200)
        preview_layout.addWidget(self.preview_view)

        self.preview_info_label = QLabel()
        preview_layout.addWidget(self.preview_info_label)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # 按钮
        button_layout = QHBoxLayout()

        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self._on_export)
        button_layout.addWidget(self.export_button)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def _update_preview(self) -> None:
        """更新预览"""
        # 获取合并后的图层数据
        data = self.canvas.merge_visible_layers()

        # 获取导出参数
        scan_mode = self.scan_mode_combo.currentData()
        msb_first = self.bit_order_combo.currentData()
        invert = self.invert_checkbox.isChecked()

        # 导出为字节流
        if scan_mode == "horizontal":
            byte_data = ExportService.horizontal_scan(data, msb_first, invert)
        else:
            byte_data = ExportService.vertical_scan(data, msb_first, invert)

        # 反向解析预览
        height, width = data.shape
        preview_data = PreviewService.preview(
            byte_data, width, height, scan_mode, msb_first, invert
        )

        # 转换为图像
        image = QImage(width, height, QImage.Format.Format_Mono)
        for y in range(height):
            for x in range(width):
                color = 0 if preview_data[y, x] else 1
                image.setPixel(x, y, color)

        # 显示预览
        pixmap = QPixmap.fromImage(image)
        # 放大预览
        scale_factor = min(400 / width, 400 / height, 8)
        scaled_pixmap = pixmap.scaled(
            int(width * scale_factor),
            int(height * scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        self.preview_scene.clear()
        self.preview_scene.addPixmap(scaled_pixmap)
        self.preview_view.fitInView(self.preview_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        # 更新信息
        self.preview_info_label.setText(
            f"尺寸: {width}x{height} | 数据大小: {len(byte_data)} 字节"
        )

    def _on_export(self) -> None:
        """导出按钮点击事件"""
        filename = self.filename_edit.text()
        if not filename:
            return

        format_type = self.format_combo.currentData()

        # 选择保存路径
        if format_type == "c_array":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出 C Array", f"{filename}.h", "C Header Files (*.h)"
            )
        elif format_type == "binary":
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出 Binary", f"{filename}.bin", "Binary Files (*.bin)"
            )
        else:  # png
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出 PNG", f"{filename}.png", "PNG Images (*.png)"
            )

        if not file_path:
            return

        # 获取合并后的图层数据
        data = self.canvas.merge_visible_layers()

        # 获取导出参数
        scan_mode = self.scan_mode_combo.currentData()
        msb_first = self.bit_order_combo.currentData()
        invert = self.invert_checkbox.isChecked()

        try:
            if format_type == "c_array":
                # 导出为 C Array
                array_name = Path(file_path).stem.replace("-", "_").replace(" ", "_")
                c_code = ExportService.export_to_c_array(
                    data, array_name, scan_mode, msb_first, invert
                )
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(c_code)

            elif format_type == "binary":
                # 导出为 Binary
                byte_data = ExportService.export_to_binary(
                    data, scan_mode, msb_first, invert
                )
                with open(file_path, "wb") as f:
                    f.write(byte_data)

            else:  # png
                # 导出为 PNG（使用向量化操作提升性能）
                height, width = data.shape

                # 处理反转
                export_data = ~data if invert else data

                # 转换为 RGB 数组（True=黑色, False=白色）
                rgb_data = np.where(export_data, 0, 255).astype(np.uint8)

                # 创建 RGB 图像
                image_data = np.zeros((height, width, 3), dtype=np.uint8)
                image_data[:, :, 0] = rgb_data  # R
                image_data[:, :, 1] = rgb_data  # G
                image_data[:, :, 2] = rgb_data  # B

                # 创建 QImage
                image = QImage(image_data.data, width, height, width * 3, QImage.Format.Format_RGB888)
                image._array_ref = image_data  # 防止垃圾回收
                image.save(file_path)

            self.accept()

        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "导出失败", f"导出失败: {str(e)}")
