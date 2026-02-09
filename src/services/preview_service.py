"""预览服务"""
import numpy as np
from ..utils.bit_operations import unpack_byte_msb, unpack_byte_lsb, bytes_per_row


class PreviewService:
    """预览服务类（反向解析）"""

    @staticmethod
    def parse_horizontal(byte_data: bytes, width: int, height: int,
                        msb_first: bool, invert: bool) -> np.ndarray:
        """
        解析水平扫描数据

        Args:
            byte_data: 字节流
            width: 宽度
            height: 高度
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            位图数据
        """
        result = np.zeros((height, width), dtype=bool)
        bytes_per_line = bytes_per_row(width)

        byte_idx = 0
        for y in range(height):
            for byte_col in range(bytes_per_line):
                if byte_idx >= len(byte_data):
                    break

                # 解包字节
                if msb_first:
                    bits = unpack_byte_msb(byte_data[byte_idx])
                else:
                    bits = unpack_byte_lsb(byte_data[byte_idx])

                # 填充像素
                for bit_idx, bit in enumerate(bits):
                    x = byte_col * 8 + bit_idx
                    if x < width:
                        pixel = bit
                        if invert:
                            pixel = not pixel
                        result[y, x] = pixel

                byte_idx += 1

        return result

    @staticmethod
    def parse_vertical(byte_data: bytes, width: int, height: int,
                      msb_first: bool, invert: bool) -> np.ndarray:
        """
        解析垂直扫描数据（Page mode）

        Args:
            byte_data: 字节流
            width: 宽度
            height: 高度
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            位图数据
        """
        result = np.zeros((height, width), dtype=bool)
        pages = (height + 7) // 8

        byte_idx = 0
        for page in range(pages):
            for x in range(width):
                if byte_idx >= len(byte_data):
                    break

                # 解包字节
                if msb_first:
                    bits = unpack_byte_msb(byte_data[byte_idx])
                else:
                    bits = unpack_byte_lsb(byte_data[byte_idx])

                # 填充像素
                for bit_idx, bit in enumerate(bits):
                    y = page * 8 + bit_idx
                    if y < height:
                        pixel = bit
                        if invert:
                            pixel = not pixel
                        result[y, x] = pixel

                byte_idx += 1

        return result

    @staticmethod
    def preview(byte_data: bytes, width: int, height: int,
               scan_mode: str, msb_first: bool, invert: bool) -> np.ndarray:
        """
        预览导出数据

        Args:
            byte_data: 字节流
            width: 宽度
            height: 高度
            scan_mode: 扫描模式（horizontal/vertical）
            msb_first: 是否 MSB first
            invert: 是否反色

        Returns:
            位图数据
        """
        if scan_mode == "horizontal":
            return PreviewService.parse_horizontal(byte_data, width, height, msb_first, invert)
        else:
            return PreviewService.parse_vertical(byte_data, width, height, msb_first, invert)
