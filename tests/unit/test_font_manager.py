"""测试字体管理器"""
import pytest
from src.services.font_manager import FontManager


@pytest.fixture
def font_manager(qapp):
    """创建字体管理器 fixture"""
    return FontManager()


def test_font_manager_initialization(font_manager):
    """测试字体管理器初始化"""
    assert font_manager.font_database is not None
    assert font_manager.custom_fonts == []


def test_get_system_fonts(font_manager):
    """测试获取系统字体"""
    fonts = font_manager.get_system_fonts()

    assert isinstance(fonts, list)
    assert len(fonts) > 0


def test_get_monospace_fonts(font_manager):
    """测试获取等宽字体"""
    monospace_fonts = font_manager.get_monospace_fonts()

    assert isinstance(monospace_fonts, list)
    # 应该有一些等宽字体
    assert len(monospace_fonts) >= 0


def test_create_font(font_manager):
    """测试创建字体"""
    # 创建普通字体
    font = font_manager.create_font("Arial", 12, bold=False)
    assert font.pointSize() == 12
    assert not font.bold()

    # 创建粗体字体
    font_bold = font_manager.create_font("Arial", 16, bold=True)
    assert font_bold.pointSize() == 16
    assert font_bold.bold()


def test_is_fullwidth_char(font_manager):
    """测试全角字符判断"""
    # 半角字符
    assert font_manager.is_fullwidth_char('a') is False
    assert font_manager.is_fullwidth_char('A') is False
    assert font_manager.is_fullwidth_char('1') is False
    assert font_manager.is_fullwidth_char(' ') is False

    # 全角字符
    assert font_manager.is_fullwidth_char('中') is True
    assert font_manager.is_fullwidth_char('文') is True
    assert font_manager.is_fullwidth_char('あ') is True  # 平假名
    assert font_manager.is_fullwidth_char('ア') is True  # 片假名

    # 全角 ASCII
    assert font_manager.is_fullwidth_char('Ａ') is True

    # 空字符
    assert font_manager.is_fullwidth_char('') is False


def test_is_fullwidth_char_mixed(font_manager):
    """测试混合字符"""
    test_cases = [
        ('a', False),
        ('中', True),
        ('!', False),
        ('！', True),
        ('0', False),
        ('０', True),
    ]

    for char, expected in test_cases:
        assert font_manager.is_fullwidth_char(char) == expected, f"Failed for char: {char}"
