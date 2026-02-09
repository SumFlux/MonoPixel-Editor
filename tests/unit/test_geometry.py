"""测试几何工具函数"""
import pytest
from src.utils.geometry import (
    bresenham_line, bresenham_circle, filled_circle,
    rectangle_outline, filled_rectangle, snap_to_angle,
    make_square, flood_fill
)
import numpy as np


def test_bresenham_line():
    """测试 Bresenham 直线算法"""
    # 水平线
    points = bresenham_line(0, 0, 5, 0)
    assert len(points) == 6
    assert points[0] == (0, 0)
    assert points[-1] == (5, 0)

    # 垂直线
    points = bresenham_line(0, 0, 0, 5)
    assert len(points) == 6
    assert points[0] == (0, 0)
    assert points[-1] == (0, 5)

    # 对角线
    points = bresenham_line(0, 0, 5, 5)
    assert len(points) == 6
    assert points[0] == (0, 0)
    assert points[-1] == (5, 5)


def test_bresenham_circle():
    """测试 Bresenham 圆形算法"""
    # 半径为 5 的圆
    points = bresenham_circle(10, 10, 5)
    assert len(points) > 0

    # 所有点应该在圆周上
    for x, y in points:
        distance = ((x - 10) ** 2 + (y - 10) ** 2) ** 0.5
        assert 4.5 <= distance <= 5.5  # 允许一定误差


def test_filled_circle():
    """测试填充圆形"""
    points = filled_circle(10, 10, 5)
    assert len(points) > 0

    # 所有点应该在圆内
    for x, y in points:
        distance_sq = (x - 10) ** 2 + (y - 10) ** 2
        assert distance_sq <= 25  # 半径的平方


def test_rectangle_outline():
    """测试矩形轮廓"""
    points = rectangle_outline(0, 0, 5, 3)

    # 检查四个角点
    assert (0, 0) in points
    assert (5, 0) in points
    assert (0, 3) in points
    assert (5, 3) in points

    # 轮廓点数应该是周长
    expected_count = 2 * (6 + 4) - 4  # 去除重复的角点
    assert len(points) == expected_count


def test_filled_rectangle():
    """测试填充矩形"""
    points = filled_rectangle(0, 0, 5, 3)

    # 填充点数应该是面积
    assert len(points) == 6 * 4  # (5-0+1) * (3-0+1)

    # 检查所有点都在矩形内
    for x, y in points:
        assert 0 <= x <= 5
        assert 0 <= y <= 3


def test_snap_to_angle():
    """测试角度锁定"""
    # 水平线
    x, y = snap_to_angle(0, 0, 10, 2)
    assert abs(y) < 3  # 应该接近水平

    # 垂直线
    x, y = snap_to_angle(0, 0, 2, 10)
    assert abs(x) < 3  # 应该接近垂直

    # 45度线
    x, y = snap_to_angle(0, 0, 10, 10)
    assert abs(x - y) < 2  # 应该接近对角线


def test_make_square():
    """测试正方形调整"""
    # 矩形调整为正方形
    x, y = make_square(0, 0, 10, 5)
    assert abs(x) == abs(y)  # 应该是正方形

    # 负方向
    x, y = make_square(0, 0, -10, -5)
    assert abs(x) == abs(y)


def test_flood_fill():
    """测试泛洪填充"""
    # 创建一个简单的测试图像
    data = np.zeros((10, 10), dtype=bool)

    # 绘制一个边框
    data[0, :] = True
    data[-1, :] = True
    data[:, 0] = True
    data[:, -1] = True

    # 填充中心区域
    points = flood_fill(data, 5, 5, False, True)

    # 应该填充中心的所有白色像素
    assert len(points) == 8 * 8  # 10x10 - 边框

    # 边界不应该被填充
    assert (0, 0) not in points
    assert (9, 9) not in points


def test_flood_fill_no_change():
    """测试泛洪填充（目标值等于填充值）"""
    data = np.zeros((10, 10), dtype=bool)

    # 填充值等于目标值，不应该填充
    points = flood_fill(data, 5, 5, False, False)
    assert len(points) == 0


def test_flood_fill_boundary():
    """测试泛洪填充边界检查"""
    data = np.zeros((10, 10), dtype=bool)

    # 超出边界
    points = flood_fill(data, -1, 0, False, True)
    assert len(points) == 0

    points = flood_fill(data, 0, -1, False, True)
    assert len(points) == 0

    points = flood_fill(data, 10, 0, False, True)
    assert len(points) == 0

    points = flood_fill(data, 0, 10, False, True)
    assert len(points) == 0
