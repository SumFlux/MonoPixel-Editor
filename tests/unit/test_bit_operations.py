"""测试位运算工具"""
import pytest
from src.utils.bit_operations import (
    pack_bits_msb, pack_bits_lsb, unpack_byte_msb, unpack_byte_lsb,
    pad_to_byte_boundary, bytes_per_row
)


def test_pack_bits_msb():
    """测试 MSB first 打包"""
    # 全 0
    assert pack_bits_msb([False] * 8) == 0x00

    # 全 1
    assert pack_bits_msb([True] * 8) == 0xFF

    # 第一位为 1
    assert pack_bits_msb([True, False, False, False, False, False, False, False]) == 0x80

    # 最后一位为 1
    assert pack_bits_msb([False, False, False, False, False, False, False, True]) == 0x01

    # 交替
    assert pack_bits_msb([True, False, True, False, True, False, True, False]) == 0xAA


def test_pack_bits_lsb():
    """测试 LSB first 打包"""
    # 全 0
    assert pack_bits_lsb([False] * 8) == 0x00

    # 全 1
    assert pack_bits_lsb([True] * 8) == 0xFF

    # 第一位为 1
    assert pack_bits_lsb([True, False, False, False, False, False, False, False]) == 0x01

    # 最后一位为 1
    assert pack_bits_lsb([False, False, False, False, False, False, False, True]) == 0x80

    # 交替
    assert pack_bits_lsb([True, False, True, False, True, False, True, False]) == 0x55


def test_unpack_byte_msb():
    """测试 MSB first 解包"""
    # 全 0
    bits = unpack_byte_msb(0x00)
    assert bits == [False] * 8

    # 全 1
    bits = unpack_byte_msb(0xFF)
    assert bits == [True] * 8

    # 第一位为 1
    bits = unpack_byte_msb(0x80)
    assert bits[0] == True
    assert all(not b for b in bits[1:])

    # 最后一位为 1
    bits = unpack_byte_msb(0x01)
    assert bits[-1] == True
    assert all(not b for b in bits[:-1])


def test_unpack_byte_lsb():
    """测试 LSB first 解包"""
    # 全 0
    bits = unpack_byte_lsb(0x00)
    assert bits == [False] * 8

    # 全 1
    bits = unpack_byte_lsb(0xFF)
    assert bits == [True] * 8

    # 第一位为 1
    bits = unpack_byte_lsb(0x01)
    assert bits[0] == True
    assert all(not b for b in bits[1:])

    # 最后一位为 1
    bits = unpack_byte_lsb(0x80)
    assert bits[-1] == True
    assert all(not b for b in bits[:-1])


def test_pack_unpack_roundtrip_msb():
    """测试 MSB 打包解包往返"""
    original = [True, False, True, True, False, False, True, False]
    packed = pack_bits_msb(original)
    unpacked = unpack_byte_msb(packed)
    assert unpacked == original


def test_pack_unpack_roundtrip_lsb():
    """测试 LSB 打包解包往返"""
    original = [True, False, True, True, False, False, True, False]
    packed = pack_bits_lsb(original)
    unpacked = unpack_byte_lsb(packed)
    assert unpacked == original


def test_pad_to_byte_boundary():
    """测试字节对齐"""
    assert pad_to_byte_boundary(0) == 0
    assert pad_to_byte_boundary(1) == 8
    assert pad_to_byte_boundary(7) == 8
    assert pad_to_byte_boundary(8) == 8
    assert pad_to_byte_boundary(9) == 16
    assert pad_to_byte_boundary(15) == 16
    assert pad_to_byte_boundary(16) == 16


def test_bytes_per_row():
    """测试每行字节数"""
    assert bytes_per_row(0) == 0
    assert bytes_per_row(1) == 1
    assert bytes_per_row(7) == 1
    assert bytes_per_row(8) == 1
    assert bytes_per_row(9) == 2
    assert bytes_per_row(15) == 2
    assert bytes_per_row(16) == 2
    assert bytes_per_row(17) == 3
