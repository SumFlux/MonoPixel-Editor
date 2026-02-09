"""位运算工具函数"""
import numpy as np
from typing import List


def pack_bits_msb(bits: List[bool]) -> int:
    """
    将位列表打包为字节（MSB first）

    Args:
        bits: 位列表（最多 8 位）

    Returns:
        打包后的字节值
    """
    byte_val = 0
    for i, bit in enumerate(bits[:8]):
        if bit:
            byte_val |= (1 << (7 - i))
    return byte_val


def pack_bits_lsb(bits: List[bool]) -> int:
    """
    将位列表打包为字节（LSB first）

    Args:
        bits: 位列表（最多 8 位）

    Returns:
        打包后的字节值
    """
    byte_val = 0
    for i, bit in enumerate(bits[:8]):
        if bit:
            byte_val |= (1 << i)
    return byte_val


def unpack_byte_msb(byte_val: int) -> List[bool]:
    """
    将字节解包为位列表（MSB first）

    Args:
        byte_val: 字节值

    Returns:
        位列表（8 位）
    """
    bits = []
    for i in range(8):
        bits.append(bool(byte_val & (1 << (7 - i))))
    return bits


def unpack_byte_lsb(byte_val: int) -> List[bool]:
    """
    将字节解包为位列表（LSB first）

    Args:
        byte_val: 字节值

    Returns:
        位列表（8 位）
    """
    bits = []
    for i in range(8):
        bits.append(bool(byte_val & (1 << i)))
    return bits


def pad_to_byte_boundary(width: int) -> int:
    """
    计算字节对齐后的宽度

    Args:
        width: 原始宽度

    Returns:
        对齐后的宽度（8 的倍数）
    """
    return ((width + 7) // 8) * 8


def bytes_per_row(width: int) -> int:
    """
    计算每行需要的字节数

    Args:
        width: 宽度

    Returns:
        字节数
    """
    return (width + 7) // 8
