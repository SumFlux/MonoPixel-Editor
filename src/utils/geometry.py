"""几何计算工具函数"""
from typing import List, Tuple
import numpy as np


def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """
    Bresenham 直线算法

    Args:
        x0, y0: 起点坐标
        x1, y1: 终点坐标

    Returns:
        直线上的所有像素坐标列表
    """
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0

    while True:
        points.append((x, y))

        if x == x1 and y == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return points


def bresenham_circle(cx: int, cy: int, radius: int) -> List[Tuple[int, int]]:
    """
    Bresenham 圆形算法（仅轮廓）

    Args:
        cx, cy: 圆心坐标
        radius: 半径

    Returns:
        圆形轮廓上的所有像素坐标列表
    """
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius

    while x <= y:
        # 8 个对称点
        for px, py in [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]:
            points.append((px, py))

        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    return points


def filled_circle(cx: int, cy: int, radius: int) -> List[Tuple[int, int]]:
    """
    填充圆形

    Args:
        cx, cy: 圆心坐标
        radius: 半径

    Returns:
        填充圆形的所有像素坐标列表
    """
    points = []
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                points.append((x, y))
    return points


def rectangle_outline(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """
    矩形轮廓

    Args:
        x0, y0: 左上角坐标
        x1, y1: 右下角坐标

    Returns:
        矩形轮廓的所有像素坐标列表
    """
    points = []

    # 确保坐标顺序正确
    min_x, max_x = min(x0, x1), max(x0, x1)
    min_y, max_y = min(y0, y1), max(y0, y1)

    # 上下边
    for x in range(min_x, max_x + 1):
        points.append((x, min_y))
        points.append((x, max_y))

    # 左右边（避免重复角点）
    for y in range(min_y + 1, max_y):
        points.append((min_x, y))
        points.append((max_x, y))

    return points


def filled_rectangle(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """
    填充矩形

    Args:
        x0, y0: 左上角坐标
        x1, y1: 右下角坐标

    Returns:
        填充矩形的所有像素坐标列表
    """
    points = []

    # 确保坐标顺序正确
    min_x, max_x = min(x0, x1), max(x0, x1)
    min_y, max_y = min(y0, y1), max(y0, y1)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            points.append((x, y))

    return points


def snap_to_angle(x0: int, y0: int, x1: int, y1: int) -> Tuple[int, int]:
    """
    将直线锁定到最近的 45 度角（水平、垂直、对角线）

    Args:
        x0, y0: 起点坐标
        x1, y1: 终点坐标

    Returns:
        调整后的终点坐标
    """
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) < 1 and abs(dy) < 1:
        return (x1, y1)

    # 计算角度
    angle = np.arctan2(dy, dx)
    angle_deg = np.degrees(angle)

    # 锁定到 0°, 45°, 90°, 135°, 180°, -45°, -90°, -135°
    snap_angles = [0, 45, 90, 135, 180, -45, -90, -135]
    closest_angle = min(snap_angles, key=lambda a: abs(angle_deg - a))

    # 计算距离
    distance = np.sqrt(dx ** 2 + dy ** 2)

    # 根据锁定角度计算新终点
    rad = np.radians(closest_angle)
    new_x = x0 + int(distance * np.cos(rad))
    new_y = y0 + int(distance * np.sin(rad))

    return (new_x, new_y)


def make_square(x0: int, y0: int, x1: int, y1: int) -> Tuple[int, int]:
    """
    将矩形调整为正方形（保持起点，调整终点）

    Args:
        x0, y0: 起点坐标
        x1, y1: 终点坐标

    Returns:
        调整后的终点坐标
    """
    dx = x1 - x0
    dy = y1 - y0

    # 使用较大的边长
    side = max(abs(dx), abs(dy))

    new_x = x0 + (side if dx >= 0 else -side)
    new_y = y0 + (side if dy >= 0 else -side)

    return (new_x, new_y)


def flood_fill(data: np.ndarray, x: int, y: int, target_value: bool, fill_value: bool) -> List[Tuple[int, int]]:
    """
    泛洪填充算法（4-连通）

    Args:
        data: 位图数据
        x, y: 起始坐标
        target_value: 要替换的目标值
        fill_value: 填充值

    Returns:
        被填充的所有像素坐标列表
    """
    height, width = data.shape

    # 边界检查
    if not (0 <= x < width and 0 <= y < height):
        return []

    # 如果起始点不是目标值，或者目标值等于填充值，则不填充
    if data[y, x] != target_value or target_value == fill_value:
        return []

    filled_points = []
    stack = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()

        if (cx, cy) in visited:
            continue

        if not (0 <= cx < width and 0 <= cy < height):
            continue

        if data[cy, cx] != target_value:
            continue

        visited.add((cx, cy))
        filled_points.append((cx, cy))

        # 4-连通
        stack.extend([
            (cx + 1, cy),
            (cx - 1, cy),
            (cx, cy + 1),
            (cx, cy - 1)
        ])

    return filled_points
