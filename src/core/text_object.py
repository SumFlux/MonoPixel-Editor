"""文本对象数据模型"""
from typing import Optional


class TextObject:
    """文本对象类 - 存储可编辑的文本属性"""

    def __init__(
        self,
        text: str,
        font_name: str,
        font_size: int,
        position: tuple[int, int],
        max_width: int = 0,
        letter_spacing: int = 0,
        line_spacing: int = 0,
        custom_font_path: str = ""
    ):
        """
        初始化文本对象

        Args:
            text: 文本内容
            font_name: 字体名称
            font_size: 字号（像素）
            position: 位置 (x, y)
            max_width: 最大宽度（0 = 不限制）
            letter_spacing: 字间距（像素）
            line_spacing: 行间距（像素）
            custom_font_path: 自定义字体路径
        """
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.position = position
        self.max_width = max_width
        self.letter_spacing = letter_spacing
        self.line_spacing = line_spacing
        self.custom_font_path = custom_font_path

    def copy(self) -> 'TextObject':
        """
        复制文本对象

        Returns:
            新的文本对象
        """
        return TextObject(
            text=self.text,
            font_name=self.font_name,
            font_size=self.font_size,
            position=self.position,
            max_width=self.max_width,
            letter_spacing=self.letter_spacing,
            line_spacing=self.line_spacing,
            custom_font_path=self.custom_font_path
        )

    def to_dict(self) -> dict:
        """
        转换为字典（用于序列化）

        Returns:
            字典表示
        """
        return {
            'text': self.text,
            'font_name': self.font_name,
            'font_size': self.font_size,
            'position': list(self.position),
            'max_width': self.max_width,
            'letter_spacing': self.letter_spacing,
            'line_spacing': self.line_spacing,
            'custom_font_path': self.custom_font_path
        }

    @staticmethod
    def from_dict(data: dict) -> 'TextObject':
        """
        从字典创建文本对象（用于反序列化）

        Args:
            data: 字典数据

        Returns:
            文本对象
        """
        return TextObject(
            text=data.get('text', ''),
            font_name=data.get('font_name', 'Arial'),
            font_size=data.get('font_size', 16),
            position=tuple(data.get('position', [0, 0])),
            max_width=data.get('max_width', 0),
            letter_spacing=data.get('letter_spacing', 0),
            line_spacing=data.get('line_spacing', 0),
            custom_font_path=data.get('custom_font_path', '')
        )
