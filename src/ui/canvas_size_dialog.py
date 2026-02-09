"""画布尺寸对话框"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton


class CanvasSizeDialog(QDialog):
    """画布尺寸对话框"""

    def __init__(self, current_width: int, current_height: int, parent=None):
        """
        初始化对话框

        Args:
            current_width: 当前宽度
            current_height: 当前高度
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("画布大小")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # 宽度输入
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("宽度:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.width_spin.setValue(current_width)
        width_layout.addWidget(self.width_spin)
        width_layout.addWidget(QLabel("像素"))
        layout.addLayout(width_layout)

        # 高度输入
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("高度:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.height_spin.setValue(current_height)
        height_layout.addWidget(self.height_spin)
        height_layout.addWidget(QLabel("像素"))
        layout.addLayout(height_layout)

        # 按钮
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def get_size(self):
        """
        获取输入的尺寸

        Returns:
            (width, height) 元组
        """
        return self.width_spin.value(), self.height_spin.value()
