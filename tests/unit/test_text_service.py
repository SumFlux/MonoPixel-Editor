"""测试文本渲染服务"""
import pytest
import numpy as np
from PyQt6.QtGui import QFont
from src.services.font_manager import FontManager
from src.services.text_service import TextService


@pytest.fixture
def text_service(qapp):
    """创建文本服务 fixture"""
    fm = FontManager()
    return TextService(fm)


def test_text_service_initialization(text_service):
    """测试文本服务初始化"""
    assert text_service.font_manager is not None


def test_render_empty_text(text_service):
    """测试渲染空文本"""
    font = QFont("Arial", 12)
    bitmap = text_service.render_text("", font)
    assert bitmap.shape == (1, 1)


def test_render_simple_text(text_service):
    """测试渲染简单文本"""
    font = QFont("Arial", 12)
    bitmap = text_service.render_text("A", font, squeeze_halfwidth=False)

    # 应该有一定的尺寸
    assert bitmap.shape[0] > 0
    assert bitmap.shape[1] > 0


def test_render_text_with_squeeze(text_service):
    """测试带挤压的文本渲染"""
    font = QFont("Arial", 12)

    # 不挤压
    bitmap_no_squeeze = text_service.render_text("ABC", font, squeeze_halfwidth=False)

    # 挤压
    bitmap_squeeze = text_service.render_text("ABC", font, squeeze_halfwidth=True)

    # 挤压后宽度应该更小
    assert bitmap_squeeze.shape[1] < bitmap_no_squeeze.shape[1]


def test_get_text_bounds(text_service):
    """测试获取文本边界"""
    font = QFont("Arial", 12)

    # 空文本
    width, height = text_service.get_text_bounds("", font)
    assert width == 0
    assert height == 0

    # 单个字符
    width, height = text_service.get_text_bounds("A", font)
    assert width > 0
    assert height > 0


def test_get_text_bounds_with_squeeze(text_service):
    """测试带挤压的文本边界"""
    font = QFont("Arial", 12)

    # 不挤压
    width_no_squeeze, _ = text_service.get_text_bounds("ABC", font, squeeze_halfwidth=False)

    # 挤压
    width_squeeze, _ = text_service.get_text_bounds("ABC", font, squeeze_halfwidth=True)

    # 挤压后宽度应该更小
    assert width_squeeze < width_no_squeeze


def test_calculate_squeeze_ratio(text_service):
    """测试挤压比例计算"""
    # 测试不同的字符宽度
    ratio1 = text_service._calculate_squeeze_ratio('A', 10, 12)
    assert 0.45 <= ratio1 <= 0.55

    ratio2 = text_service._calculate_squeeze_ratio('W', 15, 12)
    assert 0.45 <= ratio2 <= 0.55

    # 零宽度
    ratio3 = text_service._calculate_squeeze_ratio(' ', 0, 12)
    assert ratio3 == 0.5
