"""应用配置管理器"""
from PyQt6.QtCore import QSettings


class Config:
    """应用配置管理器"""

    def __init__(self):
        self.settings = QSettings("MonoPixelEditor", "MonoPixelEditor")

    def get_last_font_name(self) -> str:
        """获取上次使用的字体名称"""
        return self.settings.value("text/font_name", "Arial")

    def set_last_font_name(self, name: str) -> None:
        """保存字体名称"""
        self.settings.setValue("text/font_name", name)

    def get_last_font_size(self) -> int:
        """获取上次使用的字号"""
        try:
            value = self.settings.value("text/font_size", 16)
            result = int(value)
            # 验证范围（1-500）
            if not (1 <= result <= 500):
                return 16
            return result
        except (ValueError, TypeError):
            return 16

    def set_last_font_size(self, size: int) -> None:
        """保存字号"""
        self.settings.setValue("text/font_size", size)

    def get_last_custom_font_path(self) -> str:
        """获取上次使用的自定义字体路径"""
        return self.settings.value("text/custom_font_path", "")

    def set_last_custom_font_path(self, path: str) -> None:
        """保存自定义字体路径"""
        self.settings.setValue("text/custom_font_path", path)

    def get_last_max_width(self) -> int:
        """获取上次使用的最大宽度"""
        try:
            value = self.settings.value("text/max_width", 0)
            result = int(value)
            # 验证范围（不能为负数）
            if result < 0:
                return 0
            return result
        except (ValueError, TypeError):
            return 0

    def set_last_max_width(self, width: int) -> None:
        """保存最大宽度"""
        self.settings.setValue("text/max_width", width)

    def get_last_letter_spacing(self) -> int:
        """获取上次使用的字间距"""
        try:
            value = self.settings.value("text/letter_spacing", 0)
            result = int(value)
            # 限制范围（-100 到 100）
            return max(-100, min(100, result))
        except (ValueError, TypeError):
            return 0

    def set_last_letter_spacing(self, spacing: int) -> None:
        """保存字间距"""
        self.settings.setValue("text/letter_spacing", spacing)

    def get_last_line_spacing(self) -> int:
        """获取上次使用的行间距"""
        try:
            value = self.settings.value("text/line_spacing", 0)
            result = int(value)
            # 限制范围（-100 到 100）
            return max(-100, min(100, result))
        except (ValueError, TypeError):
            return 0

    def set_last_line_spacing(self, spacing: int) -> None:
        """保存行间距"""
        self.settings.setValue("text/line_spacing", spacing)
