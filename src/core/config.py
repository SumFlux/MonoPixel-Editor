"""应用配置管理器"""
from PyQt6.QtCore import QSettings


class Config:
    """应用配置管理器"""

    def __init__(self):
        self.settings = QSettings("MonoPixelEditor", "MonoPixelEditor")

    def get_last_font_name(self) -> str:
        """获取上次使用的字体名称"""
        return self.settings.value("text/font_name", "Arial")

    def set_last_font_name(self, name: str):
        """保存字体名称"""
        self.settings.setValue("text/font_name", name)

    def get_last_font_size(self) -> int:
        """获取上次使用的字号"""
        return int(self.settings.value("text/font_size", 16))

    def set_last_font_size(self, size: int):
        """保存字号"""
        self.settings.setValue("text/font_size", size)

    def get_last_custom_font_path(self) -> str:
        """获取上次使用的自定义字体路径"""
        return self.settings.value("text/custom_font_path", "")

    def set_last_custom_font_path(self, path: str):
        """保存自定义字体路径"""
        self.settings.setValue("text/custom_font_path", path)

    def get_last_max_width(self) -> int:
        """获取上次使用的最大宽度"""
        return int(self.settings.value("text/max_width", 0))

    def set_last_max_width(self, width: int):
        """保存最大宽度"""
        self.settings.setValue("text/max_width", width)

    def get_last_letter_spacing(self) -> int:
        """获取上次使用的字间距"""
        return int(self.settings.value("text/letter_spacing", 0))

    def set_last_letter_spacing(self, spacing: int):
        """保存字间距"""
        self.settings.setValue("text/letter_spacing", spacing)

    def get_last_line_spacing(self) -> int:
        """获取上次使用的行间距"""
        return int(self.settings.value("text/line_spacing", 0))

    def set_last_line_spacing(self, spacing: int):
        """保存行间距"""
        self.settings.setValue("text/line_spacing", spacing)
