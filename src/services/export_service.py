"""导出服务"""
import numpy as np
from typing import Tuple
from ..utils.bit_operations import pack_bits_msb, pack_bits_lsb, bytes_per_row


class ExportService:
    """导出服务类"""

    @staticmethod
    def horizontal_scan(data: np.ndarray, msb_first: bool = True, invert: bool = False) -> bytes:
        """
        水平扫描（逐行扫描）

        Args:
            data: 位图数据 (height, width)
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            字节流
        """
        height, width = data.shape
        bytes_per_line = bytes_per_row(width)
        result = []

        for y in range(height):
            bits = []
            for x in range(width):
                pixel = bool(data[y, x])
                if invert:
                    pixel = not pixel
                bits.append(pixel)

            # 按字节打包
            for byte_idx in range(bytes_per_line):
                start = byte_idx * 8
                end = min(start + 8, width)
                byte_bits = bits[start:end]

                # 不足 8 位补 0
                while len(byte_bits) < 8:
                    byte_bits.append(False)

                # 打包为字节
                if msb_first:
                    byte_val = pack_bits_msb(byte_bits)
                else:
                    byte_val = pack_bits_lsb(byte_bits)

                result.append(byte_val)

        return bytes(result)

    @staticmethod
    def vertical_scan(data: np.ndarray, msb_first: bool = True, invert: bool = False) -> bytes:
        """
        垂直扫描（Page mode，用于 OLED）

        每 8 行为一个 page，从上到下扫描
        每个 page 内，每列为一个字节

        Args:
            data: 位图数据 (height, width)
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            字节流
        """
        height, width = data.shape
        pages = (height + 7) // 8
        result = []

        for page in range(pages):
            for x in range(width):
                bits = []
                for bit in range(8):
                    y = page * 8 + bit
                    if y < height:
                        pixel = bool(data[y, x])
                        if invert:
                            pixel = not pixel
                        bits.append(pixel)
                    else:
                        bits.append(False)  # 超出部分补 0

                # 打包为字节
                if msb_first:
                    byte_val = pack_bits_msb(bits)
                else:
                    byte_val = pack_bits_lsb(bits)

                result.append(byte_val)

        return bytes(result)

    @staticmethod
    def export_to_c_array(data: np.ndarray, name: str, scan_mode: str,
                         msb_first: bool, invert: bool) -> str:
        """
        导出为 C 数组

        Args:
            data: 位图数据
            name: 数组名称
            scan_mode: 扫描模式（horizontal/vertical）
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            C 代码字符串
        """
        height, width = data.shape

        # 选择扫描方式
        if scan_mode == "horizontal":
            byte_data = ExportService.horizontal_scan(data, msb_first, invert)
        else:
            byte_data = ExportService.vertical_scan(data, msb_first, invert)

        # 生成 C 代码
        lines = []
        lines.append(f"// Image: {name}")
        lines.append(f"// Size: {width}x{height}")
        lines.append(f"// Scan mode: {scan_mode}")
        lines.append(f"// Bit order: {'MSB first' if msb_first else 'LSB first'}")
        lines.append(f"// Inverted: {'Yes' if invert else 'No'}")
        lines.append(f"// Data size: {len(byte_data)} bytes")
        lines.append("")
        lines.append(f"const unsigned char {name}[] = {{")

        # 每行 16 个字节
        for i in range(0, len(byte_data), 16):
            chunk = byte_data[i:i+16]
            hex_values = [f"0x{b:02X}" for b in chunk]
            line = "    " + ", ".join(hex_values)
            if i + 16 < len(byte_data):
                line += ","
            lines.append(line)

        lines.append("};")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def export_to_binary(data: np.ndarray, scan_mode: str,
                        msb_first: bool, invert: bool) -> bytes:
        """
        导出为二进制文件

        Args:
            data: 位图数据
            scan_mode: 扫描模式（horizontal/vertical）
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            字节流
        """
        if scan_mode == "horizontal":
            return ExportService.horizontal_scan(data, msb_first, invert)
        else:
            return ExportService.vertical_scan(data, msb_first, invert)
