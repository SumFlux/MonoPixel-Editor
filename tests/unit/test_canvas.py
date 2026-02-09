"""测试 Canvas 类"""
import pytest
import numpy as np
from src.core.canvas import Canvas


def test_canvas_initialization():
    """测试画布初始化"""
    canvas = Canvas(212, 104)

    assert canvas.width == 212
    assert canvas.height == 104
    assert len(canvas.layers) == 1  # 默认有一个背景图层
    assert canvas.active_layer_index == 0
    assert canvas.grid_visible is True
    assert canvas.layers[0].name == "Background"


def test_add_layer():
    """测试添加图层"""
    canvas = Canvas(100, 100)

    # 添加命名图层
    layer1 = canvas.add_layer("Layer 1")
    assert layer1.name == "Layer 1"
    assert len(canvas.layers) == 2
    assert canvas.active_layer_index == 1

    # 添加自动命名图层
    layer2 = canvas.add_layer()
    assert layer2.name == "Layer 3"
    assert len(canvas.layers) == 3
    assert canvas.active_layer_index == 2


def test_remove_layer():
    """测试删除图层"""
    canvas = Canvas(100, 100)
    canvas.add_layer("Layer 1")
    canvas.add_layer("Layer 2")

    # 删除中间图层
    assert canvas.remove_layer(1) is True
    assert len(canvas.layers) == 2

    # 不能删除最后一个图层
    canvas.remove_layer(1)
    assert canvas.remove_layer(0) is False
    assert len(canvas.layers) == 1


def test_move_layer():
    """测试移动图层"""
    canvas = Canvas(100, 100)
    layer1 = canvas.add_layer("Layer 1")
    layer2 = canvas.add_layer("Layer 2")
    layer3 = canvas.add_layer("Layer 3")

    # 初始顺序: [Background, Layer 1, Layer 2, Layer 3]
    # 向上移动 Layer 3 (索引3) 到顶部 (索引0)
    assert canvas.move_layer(3, 0) is True
    assert canvas.layers[0].name == "Layer 3"
    assert canvas.layers[1].name == "Background"
    assert canvas.layers[2].name == "Layer 1"
    assert canvas.layers[3].name == "Layer 2"

    # 向下移动 Layer 3 (现在在索引0) 到索引2
    assert canvas.move_layer(0, 2) is True
    assert canvas.layers[0].name == "Background"
    assert canvas.layers[1].name == "Layer 1"
    assert canvas.layers[2].name == "Layer 3"
    assert canvas.layers[3].name == "Layer 2"


def test_get_active_layer():
    """测试获取活动图层"""
    canvas = Canvas(100, 100)

    active = canvas.get_active_layer()
    assert active is not None
    assert active.name == "Background"

    canvas.add_layer("Layer 1")
    active = canvas.get_active_layer()
    assert active.name == "Layer 1"


def test_merge_visible_layers():
    """测试合并可见图层"""
    canvas = Canvas(10, 10)

    # 在不同图层绘制像素
    canvas.layers[0].set_pixel(0, 0, True)

    layer1 = canvas.add_layer("Layer 1")
    layer1.set_pixel(5, 5, True)

    layer2 = canvas.add_layer("Layer 2")
    layer2.set_pixel(9, 9, True)

    # 合并所有可见图层
    merged = canvas.merge_visible_layers()
    assert merged[0, 0] == True
    assert merged[5, 5] == True
    assert merged[9, 9] == True

    # 隐藏中间图层
    layer1.visible = False
    merged = canvas.merge_visible_layers()
    assert merged[0, 0] == True
    assert merged[5, 5] == False  # 被隐藏
    assert merged[9, 9] == True


def test_resize():
    """测试调整画布大小"""
    canvas = Canvas(100, 100)
    layer = canvas.get_active_layer()
    layer.set_pixel(50, 50, True)
    layer.set_pixel(99, 99, True)

    # 放大
    canvas.resize(200, 200)
    assert canvas.width == 200
    assert canvas.height == 200
    assert layer.width == 200
    assert layer.height == 200
    assert layer.get_pixel(50, 50) == True
    assert layer.get_pixel(99, 99) == True

    # 缩小（会裁剪）
    canvas.resize(80, 80)
    assert canvas.width == 80
    assert canvas.height == 80
    assert layer.get_pixel(50, 50) == True
    assert layer.get_pixel(79, 79) == False  # 超出范围
