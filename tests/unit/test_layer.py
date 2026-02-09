"""测试 Layer 类"""
import pytest
import numpy as np
from src.core.layer import Layer


def test_layer_initialization():
    """测试图层初始化"""
    layer = Layer(100, 50, "Test Layer")

    assert layer.name == "Test Layer"
    assert layer.width == 100
    assert layer.height == 50
    assert layer.visible is True
    assert layer.locked is False
    assert layer.data.shape == (50, 100)
    assert layer.data.dtype == bool
    assert not layer.data.any()  # 所有像素应该是 False（白色）


def test_set_and_get_pixel():
    """测试设置和获取像素"""
    layer = Layer(10, 10)

    # 设置像素
    layer.set_pixel(5, 5, True)
    assert layer.get_pixel(5, 5) == True

    layer.set_pixel(5, 5, False)
    assert layer.get_pixel(5, 5) == False

    # 边界外的像素
    layer.set_pixel(-1, 0, True)
    layer.set_pixel(0, -1, True)
    layer.set_pixel(10, 0, True)
    layer.set_pixel(0, 10, True)
    assert not layer.data.any()  # 不应该有任何像素被设置


def test_clear():
    """测试清空图层"""
    layer = Layer(10, 10)

    # 设置一些像素
    layer.set_pixel(0, 0, True)
    layer.set_pixel(5, 5, True)
    layer.set_pixel(9, 9, True)
    assert layer.data.any()

    # 清空
    layer.clear()
    assert not layer.data.any()


def test_copy():
    """测试复制图层"""
    layer = Layer(10, 10, "Original")
    layer.set_pixel(5, 5, True)
    layer.visible = False
    layer.locked = True

    # 复制
    copy = layer.copy()

    assert copy.name == "Original Copy"
    assert copy.width == layer.width
    assert copy.height == layer.height
    assert copy.visible == layer.visible
    assert copy.locked == layer.locked
    assert np.array_equal(copy.data, layer.data)

    # 修改副本不应影响原图层
    copy.set_pixel(0, 0, True)
    assert layer.get_pixel(0, 0) == False


def test_get_bounds():
    """测试获取边界框"""
    layer = Layer(100, 100)

    # 空图层
    bounds = layer.get_bounds()
    assert bounds == (0, 0, 0, 0)

    # 单个像素
    layer.set_pixel(50, 50, True)
    bounds = layer.get_bounds()
    assert bounds == (50, 50, 51, 51)

    # 矩形区域
    layer.clear()
    for x in range(10, 20):
        for y in range(30, 40):
            layer.set_pixel(x, y, True)

    bounds = layer.get_bounds()
    assert bounds == (10, 30, 20, 40)
