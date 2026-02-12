"""测试画布渲染性能优化"""
import sys
import time
import numpy as np
from PyQt6.QtWidgets import QApplication
from src.core.canvas import Canvas
from src.ui.canvas_view import CanvasView

# 设置输出编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_rendering_performance():
    """测试渲染性能"""
    print("=" * 60)
    print("画布渲染性能测试")
    print("=" * 60)

    # 创建应用
    app = QApplication(sys.argv)

    # 测试不同尺寸的画布
    test_sizes = [
        (128, 128, "小画布"),
        (512, 512, "中画布"),
        (1024, 768, "大画布"),
    ]

    for width, height, desc in test_sizes:
        print(f"\n测试 {desc} ({width}x{height}):")
        print("-" * 60)

        # 创建画布
        canvas = Canvas(width, height)

        # 添加一些测试数据
        layer = canvas.get_active_layer()
        if layer and layer.data is not None:
            # 创建一些随机像素
            layer.data = np.random.choice([True, False], size=(height, width), p=[0.3, 0.7])

        # 创建视图
        view = CanvasView(canvas)

        # 测试渲染性能（多次渲染取平均值）
        num_iterations = 10
        total_time = 0

        for i in range(num_iterations):
            start_time = time.perf_counter()
            view.update_canvas()
            end_time = time.perf_counter()
            total_time += (end_time - start_time)

        avg_time = total_time / num_iterations
        pixels = width * height

        print(f"  像素总数: {pixels:,}")
        print(f"  平均渲染时间: {avg_time*1000:.2f} ms")
        print(f"  渲染速度: {pixels/avg_time:,.0f} 像素/秒")

        # 验证渲染结果
        if view.canvas_item:
            pixmap = view.canvas_item.pixmap()
            print(f"  渲染结果: {pixmap.width()}x{pixmap.height()} 像素")
            print(f"  ✓ 渲染成功")
        else:
            print(f"  ✗ 渲染失败")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


def test_color_correctness():
    """测试颜色正确性"""
    print("\n" + "=" * 60)
    print("颜色正确性测试")
    print("=" * 60)

    # 创建应用
    app = QApplication(sys.argv)

    # 创建小画布用于测试
    canvas = Canvas(4, 4)
    layer = canvas.get_active_layer()

    if layer and layer.data is not None:
        # 创建测试图案
        # True = 黑色, False = 白色
        layer.data = np.array([
            [True,  False, True,  False],
            [False, True,  False, True ],
            [True,  False, True,  False],
            [False, True,  False, True ]
        ], dtype=bool)

    # 创建视图并渲染
    view = CanvasView(canvas)
    view.update_canvas()

    # 检查渲染结果
    if view.canvas_item:
        pixmap = view.canvas_item.pixmap()
        image = pixmap.toImage()

        print("\n检查像素颜色:")
        print("-" * 60)

        # 检查几个关键像素
        test_pixels = [
            (0, 0, True,  "黑色"),  # 应该是黑色
            (1, 0, False, "白色"),  # 应该是白色
            (0, 1, False, "白色"),  # 应该是白色
            (1, 1, True,  "黑色"),  # 应该是黑色
        ]

        all_correct = True
        for x, y, expected_black, expected_desc in test_pixels:
            pixel = image.pixel(x, y)
            # 提取 RGB 值
            r = (pixel >> 16) & 0xFF
            g = (pixel >> 8) & 0xFF
            b = pixel & 0xFF

            is_black = (r == 0 and g == 0 and b == 0)
            is_white = (r == 255 and g == 255 and b == 255)

            if expected_black:
                if is_black:
                    print(f"  像素 ({x},{y}): ✓ 正确 (黑色: RGB={r},{g},{b})")
                else:
                    print(f"  像素 ({x},{y}): ✗ 错误 (期望黑色，实际: RGB={r},{g},{b})")
                    all_correct = False
            else:
                if is_white:
                    print(f"  像素 ({x},{y}): ✓ 正确 (白色: RGB={r},{g},{b})")
                else:
                    print(f"  像素 ({x},{y}): ✗ 错误 (期望白色，实际: RGB={r},{g},{b})")
                    all_correct = False

        print("-" * 60)
        if all_correct:
            print("✓ 所有颜色测试通过")
        else:
            print("✗ 部分颜色测试失败")
    else:
        print("✗ 渲染失败")

    print("=" * 60)


if __name__ == "__main__":
    test_rendering_performance()
    test_color_correctness()
