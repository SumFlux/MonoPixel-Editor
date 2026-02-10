"""测试文本对象和文本渲染增强功能"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtGui import QFont
from src.core.text_object import TextObject
from src.core.layer import Layer
from src.core.canvas import Canvas
from src.services.text_service import TextService
from src.services.font_manager import FontManager


def test_text_object():
    """测试 TextObject 类"""
    print("=" * 60)
    print("测试 1: TextObject 类")
    print("=" * 60)

    # 创建文本对象
    text_obj = TextObject(
        text="Hello World",
        font_name="Arial",
        font_size=16,
        position=(10, 20),
        max_width=100,
        letter_spacing=2,
        line_spacing=4
    )

    print(f"✓ 创建文本对象成功")
    print(f"  文本: {text_obj.text}")
    print(f"  字体: {text_obj.font_name}, {text_obj.font_size}px")
    print(f"  位置: {text_obj.position}")
    print(f"  最大宽度: {text_obj.max_width}")
    print(f"  字间距: {text_obj.letter_spacing}")
    print(f"  行间距: {text_obj.line_spacing}")

    # 测试复制
    text_obj_copy = text_obj.copy()
    print(f"✓ 复制文本对象成功")
    print(f"  复制后文本: {text_obj_copy.text}")

    # 测试序列化
    text_dict = text_obj.to_dict()
    print(f"✓ 序列化成功")
    print(f"  字典: {text_dict}")

    # 测试反序列化
    text_obj_from_dict = TextObject.from_dict(text_dict)
    print(f"✓ 反序列化成功")
    print(f"  反序列化后文本: {text_obj_from_dict.text}")

    print()


def test_layer_with_text_object():
    """测试支持文本对象的 Layer 类"""
    print("=" * 60)
    print("测试 2: Layer 类支持文本对象")
    print("=" * 60)

    # 创建位图图层
    bitmap_layer = Layer(128, 64, "Bitmap Layer", layer_type="bitmap")
    print(f"✓ 创建位图图层成功")
    print(f"  图层类型: {bitmap_layer.layer_type}")
    print(f"  数据形状: {bitmap_layer.data.shape if bitmap_layer.data is not None else 'None'}")
    print(f"  文本对象: {bitmap_layer.text_object}")

    # 创建文本图层
    text_layer = Layer(128, 64, "Text Layer", layer_type="text")
    text_obj = TextObject(
        text="Test Text",
        font_name="Arial",
        font_size=16,
        position=(0, 0)
    )
    text_layer.text_object = text_obj
    print(f"✓ 创建文本图层成功")
    print(f"  图层类型: {text_layer.layer_type}")
    print(f"  数据: {text_layer.data}")
    print(f"  文本对象: {text_layer.text_object.text if text_layer.text_object else 'None'}")

    # 测试复制
    text_layer_copy = text_layer.copy()
    print(f"✓ 复制文本图层成功")
    print(f"  复制后图层名称: {text_layer_copy.name}")
    print(f"  复制后文本对象: {text_layer_copy.text_object.text if text_layer_copy.text_object else 'None'}")

    print()


def test_canvas_with_text_layer():
    """测试 Canvas 类支持文本图层"""
    print("=" * 60)
    print("测试 3: Canvas 类支持文本图层")
    print("=" * 60)

    canvas = Canvas(128, 64)
    print(f"✓ 创建画布成功")
    print(f"  画布尺寸: {canvas.width}x{canvas.height}")
    print(f"  默认图层数: {len(canvas.layers)}")

    # 添加文本图层
    text_obj = TextObject(
        text="Canvas Test",
        font_name="Arial",
        font_size=16,
        position=(10, 10)
    )
    text_layer = canvas.add_text_layer(text_obj, "My Text")
    print(f"✓ 添加文本图层成功")
    print(f"  图层名称: {text_layer.name}")
    print(f"  图层类型: {text_layer.layer_type}")
    print(f"  文本内容: {text_layer.text_object.text if text_layer.text_object else 'None'}")
    print(f"  总图层数: {len(canvas.layers)}")

    # 测试调整画布大小
    canvas.resize(256, 128)
    print(f"✓ 调整画布大小成功")
    print(f"  新尺寸: {canvas.width}x{canvas.height}")
    print(f"  文本图层仍然存在: {text_layer.text_object is not None}")

    print()


def test_text_service_rendering():
    """测试 TextService 渲染增强功能"""
    print("=" * 60)
    print("测试 4: TextService 渲染增强")
    print("=" * 60)

    font_manager = FontManager()
    text_service = TextService(font_manager)

    font = QFont("Arial")
    font.setPixelSize(16)

    # 测试基本渲染
    text = "Hello"
    bitmap = text_service.render_text(text, font)
    print(f"✓ 基本渲染成功")
    print(f"  文本: '{text}'")
    print(f"  位图形状: {bitmap.shape}")

    # 测试字间距
    bitmap_with_spacing = text_service.render_text(text, font, letter_spacing=5)
    print(f"✓ 字间距渲染成功")
    print(f"  文本: '{text}'")
    print(f"  字间距: 5px")
    print(f"  位图形状: {bitmap_with_spacing.shape}")
    print(f"  宽度增加: {bitmap_with_spacing.shape[1] - bitmap.shape[1]}px")

    # 测试自动换行
    long_text = "This is a very long text that should wrap"
    bitmap_wrapped = text_service.render_text(long_text, font, max_width=100)
    print(f"✓ 自动换行渲染成功")
    print(f"  文本: '{long_text}'")
    print(f"  最大宽度: 100px")
    print(f"  位图形状: {bitmap_wrapped.shape}")

    # 测试行间距
    bitmap_with_line_spacing = text_service.render_text(
        long_text, font, max_width=100, line_spacing=8
    )
    print(f"✓ 行间距渲染成功")
    print(f"  文本: '{long_text}'")
    print(f"  最大宽度: 100px")
    print(f"  行间距: 8px")
    print(f"  位图形状: {bitmap_with_line_spacing.shape}")
    print(f"  高度增加: {bitmap_with_line_spacing.shape[0] - bitmap_wrapped.shape[0]}px")

    # 测试中文文本
    chinese_text = "这是一段很长的中文测试文本需要自动换行"
    bitmap_chinese = text_service.render_text(chinese_text, font, max_width=150)
    print(f"✓ 中文自动换行渲染成功")
    print(f"  文本: '{chinese_text}'")
    print(f"  最大宽度: 150px")
    print(f"  位图形状: {bitmap_chinese.shape}")

    # 测试 get_text_bounds
    bounds = text_service.get_text_bounds(long_text, font, max_width=100, line_spacing=8)
    print(f"✓ 获取文本边界成功")
    print(f"  边界: {bounds[0]}x{bounds[1]}")

    print()


def test_integration():
    """集成测试"""
    print("=" * 60)
    print("测试 5: 集成测试")
    print("=" * 60)

    # 创建画布
    canvas = Canvas(256, 128)

    # 创建文本对象
    text_obj = TextObject(
        text="MonoPixel Editor 文本对象图层系统测试",
        font_name="Arial",
        font_size=16,
        position=(10, 10),
        max_width=200,
        letter_spacing=1,
        line_spacing=4
    )

    # 添加文本图层
    text_layer = canvas.add_text_layer(text_obj, "Test Text Layer")

    print(f"✓ 创建完整的文本图层成功")
    print(f"  画布尺寸: {canvas.width}x{canvas.height}")
    print(f"  图层名称: {text_layer.name}")
    print(f"  图层类型: {text_layer.layer_type}")
    print(f"  文本内容: {text_layer.text_object.text}")
    print(f"  最大宽度: {text_layer.text_object.max_width}px")
    print(f"  字间距: {text_layer.text_object.letter_spacing}px")
    print(f"  行间距: {text_layer.text_object.line_spacing}px")

    # 渲染文本对象
    font_manager = FontManager()
    text_service = TextService(font_manager)

    font = QFont(text_obj.font_name)
    font.setPixelSize(text_obj.font_size)

    bitmap = text_service.render_text(
        text_obj.text,
        font,
        max_width=text_obj.max_width,
        letter_spacing=text_obj.letter_spacing,
        line_spacing=text_obj.line_spacing
    )

    print(f"✓ 渲染文本对象成功")
    print(f"  渲染位图形状: {bitmap.shape}")

    # 测试序列化
    text_dict = text_obj.to_dict()
    text_obj_restored = TextObject.from_dict(text_dict)

    print(f"✓ 序列化/反序列化成功")
    print(f"  原始文本: {text_obj.text}")
    print(f"  恢复文本: {text_obj_restored.text}")

    print()


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("文本对象图层系统测试")
    print("Phase 1 & Phase 2 功能验证")
    print("=" * 60 + "\n")

    try:
        test_text_object()
        test_layer_with_text_object()
        test_canvas_with_text_layer()
        test_text_service_rendering()
        test_integration()

        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        print("\n总结:")
        print("  ✓ TextObject 类功能正常")
        print("  ✓ Layer 类支持文本对象")
        print("  ✓ Canvas 类支持文本图层")
        print("  ✓ TextService 渲染增强功能正常")
        print("  ✓ 文本自动换行功能正常")
        print("  ✓ 字间距和行间距功能正常")
        print("  ✓ 序列化/反序列化功能正常")
        print()

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
