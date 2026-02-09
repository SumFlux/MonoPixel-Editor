"""测试历史记录管理"""
import pytest
import numpy as np
from src.core.history import History, DrawCommand, AddLayerCommand, RemoveLayerCommand, MoveLayerCommand
from src.core.canvas import Canvas
from src.core.layer import Layer


def test_history_initialization():
    """测试历史记录初始化"""
    history = History(max_size=10)
    assert history.max_size == 10
    assert len(history.commands) == 0
    assert history.current_index == -1
    assert not history.can_undo()
    assert not history.can_redo()


def test_draw_command():
    """测试绘图命令"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()

    # 创建旧数据和新数据
    old_data = layer.data.copy()
    layer.set_pixel(5, 5, True)
    new_data = layer.data.copy()

    # 创建命令
    command = DrawCommand(layer, old_data, new_data)

    # 撤销
    command.undo()
    assert layer.get_pixel(5, 5) == False

    # 执行
    command.execute()
    assert layer.get_pixel(5, 5) == True


def test_history_execute():
    """测试执行命令"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History()

    # 执行第一个命令
    old_data = layer.data.copy()
    layer.set_pixel(5, 5, True)
    new_data = layer.data.copy()
    command1 = DrawCommand(layer, old_data, new_data)
    history.execute(command1)

    assert len(history.commands) == 1
    assert history.current_index == 0
    assert history.can_undo()
    assert not history.can_redo()

    # 执行第二个命令
    old_data = layer.data.copy()
    layer.set_pixel(3, 3, True)
    new_data = layer.data.copy()
    command2 = DrawCommand(layer, old_data, new_data)
    history.execute(command2)

    assert len(history.commands) == 2
    assert history.current_index == 1


def test_history_undo():
    """测试撤销"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History()

    # 执行命令
    old_data = layer.data.copy()
    layer.set_pixel(5, 5, True)
    new_data = layer.data.copy()
    command = DrawCommand(layer, old_data, new_data)
    history.execute(command)

    assert layer.get_pixel(5, 5) == True

    # 撤销
    assert history.undo()
    assert layer.get_pixel(5, 5) == False
    assert history.current_index == -1
    assert not history.can_undo()
    assert history.can_redo()


def test_history_redo():
    """测试重做"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History()

    # 执行命令
    old_data = layer.data.copy()
    layer.set_pixel(5, 5, True)
    new_data = layer.data.copy()
    command = DrawCommand(layer, old_data, new_data)
    history.execute(command)

    # 撤销
    history.undo()
    assert layer.get_pixel(5, 5) == False

    # 重做
    assert history.redo()
    assert layer.get_pixel(5, 5) == True
    assert history.current_index == 0
    assert history.can_undo()
    assert not history.can_redo()


def test_history_multiple_undo_redo():
    """测试多次撤销/重做"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History()

    # 执行多个命令
    positions = [(1, 1), (2, 2), (3, 3), (4, 4)]
    for x, y in positions:
        old_data = layer.data.copy()
        layer.set_pixel(x, y, True)
        new_data = layer.data.copy()
        command = DrawCommand(layer, old_data, new_data)
        history.execute(command)

    # 验证所有像素都被设置
    for x, y in positions:
        assert layer.get_pixel(x, y) == True

    # 撤销两次
    history.undo()
    history.undo()
    assert layer.get_pixel(1, 1) == True
    assert layer.get_pixel(2, 2) == True
    assert layer.get_pixel(3, 3) == False
    assert layer.get_pixel(4, 4) == False

    # 重做一次
    history.redo()
    assert layer.get_pixel(3, 3) == True
    assert layer.get_pixel(4, 4) == False


def test_history_clear_redo_on_new_command():
    """测试新命令清除重做历史"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History()

    # 执行两个命令
    old_data = layer.data.copy()
    layer.set_pixel(1, 1, True)
    new_data = layer.data.copy()
    command1 = DrawCommand(layer, old_data, new_data)
    history.execute(command1)

    old_data = layer.data.copy()
    layer.set_pixel(2, 2, True)
    new_data = layer.data.copy()
    command2 = DrawCommand(layer, old_data, new_data)
    history.execute(command2)

    # 撤销一次
    history.undo()
    assert history.can_redo()

    # 执行新命令（应该清除重做历史）
    old_data = layer.data.copy()
    layer.set_pixel(3, 3, True)
    new_data = layer.data.copy()
    command3 = DrawCommand(layer, old_data, new_data)
    history.execute(command3)

    assert not history.can_redo()
    assert len(history.commands) == 2


def test_history_max_size():
    """测试历史记录大小限制"""
    canvas = Canvas(10, 10)
    layer = canvas.get_active_layer()
    history = History(max_size=3)

    # 执行 5 个命令
    for i in range(5):
        old_data = layer.data.copy()
        layer.set_pixel(i, i, True)
        new_data = layer.data.copy()
        command = DrawCommand(layer, old_data, new_data)
        history.execute(command)

    # 应该只保留最后 3 个命令
    assert len(history.commands) == 3
    assert history.current_index == 2


def test_add_layer_command():
    """测试添加图层命令"""
    canvas = Canvas(10, 10)
    history = History()

    initial_count = len(canvas.layers)

    # 执行添加图层命令
    command = AddLayerCommand(canvas, "New Layer")
    history.execute(command)

    assert len(canvas.layers) == initial_count + 1
    assert canvas.layers[-1].name == "New Layer"

    # 撤销
    history.undo()
    assert len(canvas.layers) == initial_count


def test_remove_layer_command():
    """测试删除图层命令"""
    canvas = Canvas(10, 10)
    canvas.add_layer("Layer 1")
    history = History()

    initial_count = len(canvas.layers)

    # 执行删除图层命令
    command = RemoveLayerCommand(canvas, 1)
    history.execute(command)

    assert len(canvas.layers) == initial_count - 1

    # 撤销
    history.undo()
    assert len(canvas.layers) == initial_count
    assert canvas.layers[1].name == "Layer 1"


def test_move_layer_command():
    """测试移动图层命令"""
    canvas = Canvas(10, 10)
    canvas.add_layer("Layer 1")
    canvas.add_layer("Layer 2")
    history = History()

    # 执行移动图层命令
    command = MoveLayerCommand(canvas, 0, 2)
    history.execute(command)

    assert canvas.layers[2].name == "Background"

    # 撤销
    history.undo()
    assert canvas.layers[0].name == "Background"
