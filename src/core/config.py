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
