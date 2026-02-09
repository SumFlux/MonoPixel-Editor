"""测试导出服务"""
import pytest
import numpy as np
from src.services.export_service import ExportService
from src.services.preview_service import PreviewService


def test_horizontal_scan_simple():
    """测试简单的水平扫描"""
    # 创建一个简单的 8x8 图像
    data = np.zeros((8, 8), dtype=bool)
    data[0, 0] = True  # 第一个像素

    # 水平扫描 MSB first
    result = ExportService.horizontal_scan(data, msb_first=True, invert=False)

    # 第一个字节应该是 0x80 (10000000)
    assert result[0] == 0x80
    # 其余字节应该是 0x00
    assert all(b == 0x00 for b in result[1:])


def test_horizontal_scan_full_row():
    """测试完整行的水平扫描"""
    # 创建一个 8x8 图像，第一行全黑
    data = np.zeros((8, 8), dtype=bool)
    data[0, :] = True

    # 水平扫描 MSB first
    result = ExportService.horizontal_scan(data, msb_first=True, invert=False)

    # 第一个字节应该是 0xFF
    assert result[0] == 0xFF
    # 其余字节应该是 0x00
    assert all(b == 0x00 for b in result[1:])


def test_horizontal_scan_msb_vs_lsb():
    """测试 MSB 和 LSB 的区别"""
    # 创建一个 8x1 图像，只有第一个像素为黑
    data = np.zeros((1, 8), dtype=bool)
    data[0, 0] = True

    # MSB first: 第一位在最高位
    result_msb = ExportService.horizontal_scan(data, msb_first=True, invert=False)
    assert result_msb[0] == 0x80  # 10000000

    # LSB first: 第一位在最低位
    result_lsb = ExportService.horizontal_scan(data, msb_first=False, invert=False)
    assert result_lsb[0] == 0x01  # 00000001


def test_horizontal_scan_invert():
    """测试反色"""
    # 创建一个 8x8 全白图像
    data = np.zeros((8, 8), dtype=bool)

    # 不反色：全白 -> 全 0
    result_normal = ExportService.horizontal_scan(data, msb_first=True, invert=False)
    assert all(b == 0x00 for b in result_normal)

    # 反色：全白 -> 全黑 -> 全 1
    result_inverted = ExportService.horizontal_scan(data, msb_first=True, invert=True)
    assert all(b == 0xFF for b in result_inverted)


def test_vertical_scan_simple():
    """测试简单的垂直扫描"""
    # 创建一个 8x8 图像
    data = np.zeros((8, 8), dtype=bool)
    data[0, 0] = True  # 第一列第一个像素

    # 垂直扫描 MSB first
    result = ExportService.vertical_scan(data, msb_first=True, invert=False)

    # 第一个字节应该是 0x80 (第一列的第一个 page)
    assert result[0] == 0x80
    # 其余字节应该是 0x00
    assert all(b == 0x00 for b in result[1:])


def test_vertical_scan_full_column():
    """测试完整列的垂直扫描"""
    # 创建一个 8x8 图像，第一列全黑
    data = np.zeros((8, 8), dtype=bool)
    data[:, 0] = True

    # 垂直扫描 MSB first
    result = ExportService.vertical_scan(data, msb_first=True, invert=False)

    # 第一个字节应该是 0xFF (第一列的 8 个像素)
    assert result[0] == 0xFF
    # 其余字节应该是 0x00
    assert all(b == 0x00 for b in result[1:])


def test_vertical_scan_multiple_pages():
    """测试多个 page 的垂直扫描"""
    # 创建一个 16x8 图像（2 个 pages）
    data = np.zeros((16, 8), dtype=bool)
    data[0, 0] = True   # 第一个 page 第一位
    data[8, 0] = True   # 第二个 page 第一位

    # 垂直扫描 MSB first
    result = ExportService.vertical_scan(data, msb_first=True, invert=False)

    # 第一个 page 的第一列
    assert result[0] == 0x80
    # 第二个 page 的第一列
    assert result[8] == 0x80


def test_export_to_c_array():
    """测试导出为 C 数组"""
    # 创建一个简单的 8x8 图像
    data = np.zeros((8, 8), dtype=bool)
    data[0, 0] = True

    # 导出为 C 数组
    c_code = ExportService.export_to_c_array(
        data, "test_image", "horizontal", msb_first=True, invert=False
    )

    # 检查生成的代码
    assert "const unsigned char test_image[]" in c_code
    assert "0x80" in c_code
    assert "8x8" in c_code


def test_preview_horizontal():
    """测试水平扫描预览"""
    # 创建原始数据
    original = np.zeros((8, 8), dtype=bool)
    original[0, 0] = True
    original[1, 7] = True

    # 导出
    byte_data = ExportService.horizontal_scan(original, msb_first=True, invert=False)

    # 预览（反向解析）
    preview = PreviewService.parse_horizontal(byte_data, 8, 8, msb_first=True, invert=False)

    # 应该与原始数据相同
    assert np.array_equal(preview, original)


def test_preview_vertical():
    """测试垂直扫描预览"""
    # 创建原始数据
    original = np.zeros((16, 8), dtype=bool)
    original[0, 0] = True
    original[8, 0] = True
    original[15, 7] = True

    # 导出
    byte_data = ExportService.vertical_scan(original, msb_first=True, invert=False)

    # 预览（反向解析）
    preview = PreviewService.parse_vertical(byte_data, 8, 16, msb_first=True, invert=False)

    # 应该与原始数据相同
    assert np.array_equal(preview, original)


def test_roundtrip_horizontal_msb():
    """测试水平扫描 MSB 往返"""
    # 创建随机数据
    original = np.random.randint(0, 2, (16, 24), dtype=bool)

    # 导出
    byte_data = ExportService.horizontal_scan(original, msb_first=True, invert=False)

    # 预览
    preview = PreviewService.parse_horizontal(byte_data, 24, 16, msb_first=True, invert=False)

    # 应该相同
    assert np.array_equal(preview, original)


def test_roundtrip_horizontal_lsb():
    """测试水平扫描 LSB 往返"""
    # 创建随机数据
    original = np.random.randint(0, 2, (16, 24), dtype=bool)

    # 导出
    byte_data = ExportService.horizontal_scan(original, msb_first=False, invert=False)

    # 预览
    preview = PreviewService.parse_horizontal(byte_data, 24, 16, msb_first=False, invert=False)

    # 应该相同
    assert np.array_equal(preview, original)


def test_roundtrip_vertical_msb():
    """测试垂直扫描 MSB 往返"""
    # 创建随机数据
    original = np.random.randint(0, 2, (16, 24), dtype=bool)

    # 导出
    byte_data = ExportService.vertical_scan(original, msb_first=True, invert=False)

    # 预览
    preview = PreviewService.parse_vertical(byte_data, 24, 16, msb_first=True, invert=False)

    # 应该相同
    assert np.array_equal(preview, original)


def test_roundtrip_vertical_lsb():
    """测试垂直扫描 LSB 往返"""
    # 创建随机数据
    original = np.random.randint(0, 2, (16, 24), dtype=bool)

    # 导出
    byte_data = ExportService.vertical_scan(original, msb_first=False, invert=False)

    # 预览
    preview = PreviewService.parse_vertical(byte_data, 24, 16, msb_first=False, invert=False)

    # 应该相同
    assert np.array_equal(preview, original)


def test_roundtrip_with_invert():
    """测试带反色的往返"""
    # 创建随机数据
    original = np.random.randint(0, 2, (16, 24), dtype=bool)

    # 导出（反色）
    byte_data = ExportService.horizontal_scan(original, msb_first=True, invert=True)

    # 预览（反色）
    preview = PreviewService.parse_horizontal(byte_data, 24, 16, msb_first=True, invert=True)

    # 应该相同
    assert np.array_equal(preview, original)
