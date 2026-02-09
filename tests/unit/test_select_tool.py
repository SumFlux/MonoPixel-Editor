"""选择工具单元测试"""
import pytest
import numpy as np
from PyQt6.QtCore import Qt

from src.core.canvas import Canvas
from src.tools.select import SelectTool


@pytest.fixture
def canvas():
    """创建测试画布"""
    return Canvas(20, 20)


@pytest.fixture
def select_tool(canvas):
    """创建选择工具"""
    return SelectTool(canvas)


def test_select_tool_init(select_tool):
    """测试选择工具初始化"""
    assert select_tool.selection_rect is None
    assert select_tool.selected_data is None
    assert not select_tool.is_moving
    assert not select_tool.is_resizing


def test_create_selection(canvas, select_tool):
    """测试创建选区"""
    layer = canvas.get_active_layer()

    # 在图层上绘制一些像素
    layer.data[5:10, 5:10] = True

    # 创建选区
    select_tool.on_press(5, 5, Qt.KeyboardModifier.NoModifier)
    select_tool.on_drag(10, 10, Qt.KeyboardModifier.NoModifier)
    select_tool.on_release(10, 10, Qt.KeyboardModifier.NoModifier)

    # 验证选区
    assert select_tool.selection_rect == (5, 5, 5, 5)
    assert select_tool.selected_data is not None
    assert select_tool.selected_data.shape == (5, 5)


def test_move_selection(canvas, select_tool):
    """测试移动选区"""
    layer = canvas.get_active_layer()

    # 在图层上绘制一些像素
    layer.data[5:10, 5:10] = True

    # 创建选区
    select_tool.on_press(5, 5, Qt.KeyboardModifier.NoModifier)
    select_tool.on_drag(10, 10, Qt.KeyboardModifier.NoModifier)
    select_tool.on_release(10, 10, Qt.KeyboardModifier.NoModifier)

    # 移动选区
    select_tool.on_press(7, 7, Qt.KeyboardModifier.NoModifier)  # 点击选区内
    select_tool.on_drag(12, 12, Qt.KeyboardModifier.NoModifier)  # 移动 5 像素
    select_tool.on_release(12, 12, Qt.KeyboardModifier.NoModifier)

    # 验证选区位置
    assert select_tool.selection_rect == (10, 10, 5, 5)

    # 验证原始位置已清除
    assert not np.any(layer.data[5:10, 5:10])

    # 验证新位置有数据
    assert np.any(layer.data[10:15, 10:15])


def test_scale_selection(canvas, select_tool):
    """测试缩放选区"""
    layer = canvas.get_active_layer()

    # 在图层上绘制一个 4x4 的正方形
    layer.data[5:9, 5:9] = True

    # 创建选区
    select_tool.on_press(5, 5, Qt.KeyboardModifier.NoModifier)
    select_tool.on_drag(9, 9, Qt.KeyboardModifier.NoModifier)
    select_tool.on_release(9, 9, Qt.KeyboardModifier.NoModifier)

    # 缩放选区（拖拽右下角手柄）
    select_tool.on_press(9, 9, Qt.KeyboardModifier.NoModifier)  # 点击右下角手柄
    select_tool.on_drag(13, 13, Qt.KeyboardModifier.NoModifier)  # 放大到 8x8
    select_tool.on_release(13, 13, Qt.KeyboardModifier.NoModifier)

    # 验证选区大小
    assert select_tool.selection_rect == (5, 5, 8, 8)

    # 验证缩放后的数据
    assert select_tool.selected_data.shape == (8, 8)


def test_nearest_neighbor_scaling(select_tool):
    """测试最近邻插值缩放"""
    # 创建一个 2x2 的测试数据
    data = np.array([
        [True, False],
        [False, True]
    ], dtype=bool)

    # 放大到 4x4
    scaled = select_tool._scale_selection(data, (0, 0, 4, 4))

    assert scaled.shape == (4, 4)
    # 验证最近邻插值结果
    assert scaled[0, 0] == True
    assert scaled[0, 1] == True
    assert scaled[1, 0] == True
    assert scaled[1, 1] == True
    assert scaled[2, 2] == True
    assert scaled[2, 3] == True
    assert scaled[3, 2] == True
    assert scaled[3, 3] == True


def test_is_point_in_selection(select_tool):
    """测试点是否在选区内"""
    select_tool.selection_rect = (5, 5, 10, 10)

    assert select_tool._is_point_in_selection(7, 7)
    assert select_tool._is_point_in_selection(5, 5)
    assert select_tool._is_point_in_selection(14, 14)
    assert not select_tool._is_point_in_selection(15, 15)
    assert not select_tool._is_point_in_selection(4, 4)


def test_get_handle_positions(select_tool):
    """测试获取手柄位置"""
    select_tool.selection_rect = (10, 10, 20, 20)

    handles = select_tool._get_handle_positions()

    assert handles['nw'] == (10, 10)
    assert handles['ne'] == (30, 10)
    assert handles['sw'] == (10, 30)
    assert handles['se'] == (30, 30)
    assert handles['n'] == (20, 10)
    assert handles['s'] == (20, 30)
    assert handles['w'] == (10, 20)
    assert handles['e'] == (30, 20)


def test_clear_selection(canvas, select_tool):
    """测试清除选区"""
    layer = canvas.get_active_layer()
    layer.data[5:10, 5:10] = True

    # 创建选区
    select_tool.on_press(5, 5, Qt.KeyboardModifier.NoModifier)
    select_tool.on_drag(10, 10, Qt.KeyboardModifier.NoModifier)
    select_tool.on_release(10, 10, Qt.KeyboardModifier.NoModifier)

    assert select_tool.has_selection()

    # 清除选区
    select_tool.clear_selection()

    assert not select_tool.has_selection()
    assert select_tool.selection_rect is None
    assert select_tool.selected_data is None


def test_extract_selection(canvas, select_tool):
    """测试提取选区数据"""
    layer = canvas.get_active_layer()

    # 创建一个图案
    layer.data[5:10, 5:10] = True
    layer.data[7, 7] = False

    select_tool.selection_rect = (5, 5, 5, 5)
    extracted = select_tool._extract_selection(layer.data)

    assert extracted.shape == (5, 5)
    assert np.all(extracted == layer.data[5:10, 5:10])


def test_scale_selection_down(select_tool):
    """测试缩小选区"""
    # 创建一个 4x4 的测试数据
    data = np.ones((4, 4), dtype=bool)

    # 缩小到 2x2
    scaled = select_tool._scale_selection(data, (0, 0, 2, 2))

    assert scaled.shape == (2, 2)
    assert np.all(scaled == True)


def test_calculate_resized_rect(select_tool):
    """测试计算缩放后的矩形"""
    select_tool.original_rect = (10, 10, 20, 20)

    # 测试向右下拉伸
    select_tool.resize_handle = 'se'
    new_rect = select_tool._calculate_resized_rect(35, 35)
    assert new_rect == (10, 10, 25, 25)

    # 测试向左上拉伸
    select_tool.resize_handle = 'nw'
    new_rect = select_tool._calculate_resized_rect(5, 5)
    assert new_rect == (5, 5, 25, 25)

    # 测试向右拉伸
    select_tool.resize_handle = 'e'
    new_rect = select_tool._calculate_resized_rect(35, 20)
    assert new_rect == (10, 10, 25, 20)

    # 测试向下拉伸
    select_tool.resize_handle = 's'
    new_rect = select_tool._calculate_resized_rect(20, 35)
    assert new_rect == (10, 10, 20, 25)
