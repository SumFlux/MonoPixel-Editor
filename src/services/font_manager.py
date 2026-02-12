"""字体管理器"""
from PyQt6.QtGui import QFontDatabase, QFont
from typing import List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class FontManager:
    """字体管理器类"""

    def __init__(self):
        """初始化字体管理器"""
        # PyQt6 中 QFontDatabase 是静态类，不需要实例化
        self.custom_fonts = []

    def get_system_fonts(self) -> List[str]:
        """
        获取系统字体列表

        Returns:
            字体名称列表
        """
        return QFontDatabase.families()

    def get_monospace_fonts(self) -> List[str]:
        """
        获取等宽字体列表

        Returns:
            等宽字体名称列表
        """
        all_fonts = self.get_system_fonts()
        monospace_fonts = []

        for font_name in all_fonts:
            if QFontDatabase.isFixedPitch(font_name):
                monospace_fonts.append(font_name)

        return monospace_fonts

    def load_custom_font(self, font_path: str) -> Optional[str]:
        """
        加载自定义字体文件

        Args:
            font_path: 字体文件路径（.ttf, .otf）

        Returns:
            字体名称，如果加载失败则返回 None
        """
        # 安全验证：规范化路径
        try:
            normalized_path = os.path.normpath(os.path.abspath(font_path))
        except Exception as e:
            logger.error(f"路径规范化失败: {e}")
            return None

        # 验证文件存在
        if not os.path.exists(normalized_path):
            logger.warning(f"字体文件不存在: {normalized_path}")
            return None

        # 验证是文件而非目录
        if not os.path.isfile(normalized_path):
            logger.error(f"路径不是文件: {normalized_path}")
            return None

        # 验证文件扩展名（只允许 .ttf 和 .otf）
        _, ext = os.path.splitext(normalized_path)
        if ext.lower() not in ['.ttf', '.otf']:
            logger.error(f"不支持的字体格式: {ext}")
            return None

        # 验证文件大小（限制 10MB）
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        try:
            file_size = os.path.getsize(normalized_path)
            if file_size > MAX_FILE_SIZE:
                logger.error(f"字体文件过大: {file_size} bytes (最大 {MAX_FILE_SIZE} bytes)")
                return None
        except OSError as e:
            logger.error(f"无法获取文件大小: {e}")
            return None

        # 加载字体
        font_id = QFontDatabase.addApplicationFont(normalized_path)
        if font_id == -1:
            logger.error(f"字体加载失败: {normalized_path}")
            return None

        # 获取字体名称
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_name = font_families[0]
            self.custom_fonts.append({
                'id': font_id,
                'name': font_name,
                'path': normalized_path
            })
            logger.info(f"成功加载字体: {font_name} ({normalized_path})")
            return font_name

        logger.error(f"无法获取字体名称: {normalized_path}")
        return None

    def get_custom_fonts(self) -> List[dict]:
        """
        获取已加载的自定义字体

        Returns:
            自定义字体信息列表
        """
        return self.custom_fonts

    def create_font(self, font_name: str, size: int, bold: bool = False) -> QFont:
        """
        创建字体对象

        Args:
            font_name: 字体名称
            size: 字体大小
            bold: 是否加粗

        Returns:
            QFont 对象
        """
        font = QFont(font_name, size)
        if bold:
            font.setBold(True)
        return font

    def is_fullwidth_char(self, char: str) -> bool:
        """
        判断字符是否为全角字符

        Args:
            char: 单个字符

        Returns:
            是否为全角字符
        """
        if not char:
            return False

        code = ord(char)

        # CJK 统一表意文字
        if 0x4E00 <= code <= 0x9FFF:
            return True

        # 全角 ASCII
        if 0xFF01 <= code <= 0xFF5E:
            return True

        # 其他全角字符范围
        fullwidth_ranges = [
            (0x3000, 0x303F),  # CJK 符号和标点
            (0x3040, 0x309F),  # 平假名
            (0x30A0, 0x30FF),  # 片假名
            (0xAC00, 0xD7AF),  # 韩文
        ]

        for start, end in fullwidth_ranges:
            if start <= code <= end:
                return True

        return False
