"""文本对象数据模型"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


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

        Raises:
            ValueError: 如果数据验证失败
        """
        # 验证输入类型
        if not isinstance(data, dict):
            raise ValueError(f"期望 dict 类型，得到 {type(data).__name__}")

        # 提取并验证字段
        text = data.get('text', '')
        if not isinstance(text, str):
            logger.warning(f"text 字段类型错误，期望 str，得到 {type(text).__name__}，使用默认值")
            text = ''

        font_name = data.get('font_name', 'Arial')
        if not isinstance(font_name, str):
            logger.warning(f"font_name 字段类型错误，使用默认值 'Arial'")
            font_name = 'Arial'

        font_size = data.get('font_size', 16)
        if not isinstance(font_size, int):
            try:
                font_size = int(font_size)
            except (ValueError, TypeError):
                logger.warning(f"font_size 字段类型错误，使用默认值 16")
                font_size = 16
        # 验证字号范围（1-500）
        if not (1 <= font_size <= 500):
            logger.warning(f"font_size 超出范围 ({font_size})，限制在 1-500")
            font_size = max(1, min(500, font_size))

        # 验证位置
        position_data = data.get('position', [0, 0])
        if isinstance(position_data, (list, tuple)) and len(position_data) >= 2:
            try:
                x = int(position_data[0])
                y = int(position_data[1])
                # 限制位置范围（-10000 到 10000）
                x = max(-10000, min(10000, x))
                y = max(-10000, min(10000, y))
                position = (x, y)
            except (ValueError, TypeError):
                logger.warning("position 字段值无效，使用默认值 (0, 0)")
                position = (0, 0)
        else:
            logger.warning("position 字段格式错误，使用默认值 (0, 0)")
            position = (0, 0)

        # 验证最大宽度
        max_width = data.get('max_width', 0)
        if not isinstance(max_width, int):
            try:
                max_width = int(max_width)
            except (ValueError, TypeError):
                logger.warning("max_width 字段类型错误，使用默认值 0")
                max_width = 0
        # 限制范围（0-10000）
        max_width = max(0, min(10000, max_width))

        # 验证字间距
        letter_spacing = data.get('letter_spacing', 0)
        if not isinstance(letter_spacing, int):
            try:
                letter_spacing = int(letter_spacing)
            except (ValueError, TypeError):
                logger.warning("letter_spacing 字段类型错误，使用默认值 0")
                letter_spacing = 0
        # 限制范围（-100 到 100）
        letter_spacing = max(-100, min(100, letter_spacing))

        # 验证行间距
        line_spacing = data.get('line_spacing', 0)
        if not isinstance(line_spacing, int):
            try:
                line_spacing = int(line_spacing)
            except (ValueError, TypeError):
                logger.warning("line_spacing 字段类型错误，使用默认值 0")
                line_spacing = 0
        # 限制范围（-100 到 100）
        line_spacing = max(-100, min(100, line_spacing))

        # 验证自定义字体路径
        custom_font_path = data.get('custom_font_path', '')
        if not isinstance(custom_font_path, str):
            logger.warning("custom_font_path 字段类型错误，使用默认值 ''")
            custom_font_path = ''

        return TextObject(
            text=text,
            font_name=font_name,
            font_size=font_size,
            position=position,
            max_width=max_width,
            letter_spacing=letter_spacing,
            line_spacing=line_spacing,
            custom_font_path=custom_font_path
        )
