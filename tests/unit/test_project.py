"""测试项目管理"""
import pytest
import numpy as np
import tempfile
import os
from pathlib import Path

from src.core.project import Project
from src.core.canvas import Canvas


def test_project_initialization():
    """测试项目初始化"""
    canvas = Canvas(100, 100)
    project = Project(canvas)

    assert project.canvas == canvas
    assert project.file_path is None
    assert project.modified is False


def test_encode_decode_layer_data():
    """测试图层数据编码解码"""
    # 创建测试数据
    data = np.random.randint(0, 2, (10, 10), dtype=bool)

    # 编码
    encoded = Project._encode_layer_data(data)
    assert isinstance(encoded, str)

    # 解码
    decoded = Project._decode_layer_data(encoded, 10, 10)
    assert decoded.shape == (10, 10)
    assert np.array_equal(decoded, data)


def test_save_and_load_simple():
    """测试简单的保存和加载"""
    # 创建画布
    canvas = Canvas(16, 16)
    layer = canvas.get_active_layer()
    layer.set_pixel(5, 5, True)
    layer.set_pixel(10, 10, True)

    project = Project(canvas)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        # 保存
        assert project.save(temp_path) is True
        assert project.file_path == temp_path
        assert project.modified is False

        # 创建新项目并加载
        new_canvas = Canvas(1, 1)  # 临时画布
        new_project = Project(new_canvas)
        assert new_project.load(temp_path) is True

        # 验证数据
        assert new_project.canvas.width == 16
        assert new_project.canvas.height == 16
        assert len(new_project.canvas.layers) == 1

        new_layer = new_project.canvas.get_active_layer()
        assert new_layer.get_pixel(5, 5) == True
        assert new_layer.get_pixel(10, 10) == True
        assert new_layer.get_pixel(0, 0) == False

    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_save_and_load_multiple_layers():
    """测试多图层保存和加载"""
    # 创建画布
    canvas = Canvas(20, 20)

    # 第一层
    layer1 = canvas.get_active_layer()
    layer1.name = "Background"
    layer1.set_pixel(0, 0, True)

    # 第二层
    layer2 = canvas.add_layer("Layer 1")
    layer2.set_pixel(10, 10, True)
    layer2.visible = False

    # 第三层
    layer3 = canvas.add_layer("Layer 2")
    layer3.set_pixel(15, 15, True)
    layer3.locked = True

    project = Project(canvas)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        # 保存
        assert project.save(temp_path) is True

        # 加载
        new_canvas = Canvas(1, 1)
        new_project = Project(new_canvas)
        assert new_project.load(temp_path) is True

        # 验证图层数量
        assert len(new_project.canvas.layers) == 3

        # 验证第一层
        new_layer1 = new_project.canvas.layers[0]
        assert new_layer1.name == "Background"
        assert new_layer1.get_pixel(0, 0) == True
        assert new_layer1.visible is True
        assert new_layer1.locked is False

        # 验证第二层
        new_layer2 = new_project.canvas.layers[1]
        assert new_layer2.name == "Layer 1"
        assert new_layer2.get_pixel(10, 10) == True
        assert new_layer2.visible is False
        assert new_layer2.locked is False

        # 验证第三层
        new_layer3 = new_project.canvas.layers[2]
        assert new_layer3.name == "Layer 2"
        assert new_layer3.get_pixel(15, 15) == True
        assert new_layer3.visible is True
        assert new_layer3.locked is True

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_save_and_load_canvas_settings():
    """测试画布设置保存和加载"""
    # 创建画布
    canvas = Canvas(212, 104)
    canvas.grid_visible = False
    canvas.add_layer("Layer 1")
    canvas.active_layer_index = 1

    project = Project(canvas)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        # 保存
        assert project.save(temp_path) is True

        # 加载
        new_canvas = Canvas(1, 1)
        new_project = Project(new_canvas)
        assert new_project.load(temp_path) is True

        # 验证画布设置
        assert new_project.canvas.width == 212
        assert new_project.canvas.height == 104
        assert new_project.canvas.grid_visible is False
        assert new_project.canvas.active_layer_index == 1

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_mark_modified():
    """测试修改标记"""
    canvas = Canvas(10, 10)
    project = Project(canvas)

    assert project.is_modified() is False

    project.mark_modified()
    assert project.is_modified() is True

    # 保存后应该清除修改标记
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        project.save(temp_path)
        assert project.is_modified() is False
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_get_file_name():
    """测试获取文件名"""
    canvas = Canvas(10, 10)
    project = Project(canvas)

    # 没有文件路径
    assert project.get_file_name() == "未命名"

    # 有文件路径
    project.file_path = "/path/to/my_project.mpx"
    assert project.get_file_name() == "my_project.mpx"


def test_save_large_canvas():
    """测试保存大画布"""
    # 创建较大的画布
    canvas = Canvas(200, 200)
    layer = canvas.get_active_layer()

    # 绘制一些图案
    for i in range(0, 200, 10):
        layer.set_pixel(i, i, True)

    project = Project(canvas)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        # 保存
        assert project.save(temp_path) is True

        # 加载
        new_canvas = Canvas(1, 1)
        new_project = Project(new_canvas)
        assert new_project.load(temp_path) is True

        # 验证数据
        new_layer = new_project.canvas.get_active_layer()
        for i in range(0, 200, 10):
            assert new_layer.get_pixel(i, i) == True

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_roundtrip_random_data():
    """测试随机数据往返"""
    # 创建随机数据
    canvas = Canvas(50, 50)
    layer = canvas.get_active_layer()
    layer.data = np.random.randint(0, 2, (50, 50), dtype=bool)

    project = Project(canvas)

    # 保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mpx', delete=False) as f:
        temp_path = f.name

    try:
        # 保存
        assert project.save(temp_path) is True

        # 加载
        new_canvas = Canvas(1, 1)
        new_project = Project(new_canvas)
        assert new_project.load(temp_path) is True

        # 验证数据完全相同
        new_layer = new_project.canvas.get_active_layer()
        assert np.array_equal(new_layer.data, layer.data)

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
