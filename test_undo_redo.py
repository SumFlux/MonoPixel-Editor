"""Test undo/redo functionality"""
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.canvas import Canvas
from src.core.history import History, DrawCommand
from src.core.layer import Layer

def test_undo_redo():
    """Test undo/redo functionality"""
    print("Testing undo/redo functionality...")

    # 创建画布和历史记录
    canvas = Canvas(10, 10)
    history = History()
    layer = canvas.get_active_layer()

    print(f"Initial layer data: {np.sum(layer.data)} pixels")

    # Simulate first draw
    print("\nFirst draw: set (0,0) to True")
    old_data1 = layer.data.copy()
    layer.set_pixel(0, 0, True)
    new_data1 = layer.data.copy()
    command1 = DrawCommand(layer, old_data1, new_data1)
    history.add(command1)
    print(f"After draw: {np.sum(layer.data)} pixels")

    # Simulate second draw
    print("\nSecond draw: set (1,1) to True")
    old_data2 = layer.data.copy()
    layer.set_pixel(1, 1, True)
    new_data2 = layer.data.copy()
    command2 = DrawCommand(layer, old_data2, new_data2)
    history.add(command2)
    print(f"After draw: {np.sum(layer.data)} pixels")

    # Test undo once
    print("\nUndo once...")
    if history.undo():
        print(f"After undo: {np.sum(layer.data)} pixels")
        print(f"(0,0) = {layer.get_pixel(0, 0)}, (1,1) = {layer.get_pixel(1, 1)}")
        if np.sum(layer.data) == 1 and layer.get_pixel(0, 0) and not layer.get_pixel(1, 1):
            print("[PASS] Undo once: only second draw was undone")
        else:
            print("[FAIL] Undo once: should only have (0,0) as True")
            return False
    else:
        print("[FAIL] Undo failed")
        return False

    # Test undo again
    print("\nUndo again...")
    if history.undo():
        print(f"After undo: {np.sum(layer.data)} pixels")
        print(f"(0,0) = {layer.get_pixel(0, 0)}, (1,1) = {layer.get_pixel(1, 1)}")
        if np.sum(layer.data) == 0:
            print("[PASS] Undo again: back to initial state")
        else:
            print("[FAIL] Undo again: should have no pixels")
            return False
    else:
        print("[FAIL] Undo failed")
        return False

    # Test redo
    print("\nRedo once...")
    if history.redo():
        print(f"After redo: {np.sum(layer.data)} pixels")
        print(f"(0,0) = {layer.get_pixel(0, 0)}, (1,1) = {layer.get_pixel(1, 1)}")
        if np.sum(layer.data) == 1 and layer.get_pixel(0, 0):
            print("[PASS] Redo once: restored first draw")
        else:
            print("[FAIL] Redo failed")
            return False
    else:
        print("[FAIL] Redo failed")
        return False

    # Test redo again
    print("\nRedo again...")
    if history.redo():
        print(f"After redo: {np.sum(layer.data)} pixels")
        print(f"(0,0) = {layer.get_pixel(0, 0)}, (1,1) = {layer.get_pixel(1, 1)}")
        if np.sum(layer.data) == 2 and layer.get_pixel(0, 0) and layer.get_pixel(1, 1):
            print("[PASS] Redo again: restored second draw")
        else:
            print("[FAIL] Redo again failed")
            return False
    else:
        print("[FAIL] Redo failed")
        return False

    # Test new draw after undo
    print("\nNew draw after undo...")
    history.undo()
    print(f"After undo: {np.sum(layer.data)} pixels")

    old_data3 = layer.data.copy()
    layer.set_pixel(2, 2, True)
    new_data3 = layer.data.copy()
    command3 = DrawCommand(layer, old_data3, new_data3)
    history.add(command3)
    print(f"After new draw: {np.sum(layer.data)} pixels")
    print(f"(0,0) = {layer.get_pixel(0, 0)}, (2,2) = {layer.get_pixel(2, 2)}")

    if np.sum(layer.data) == 2 and layer.get_pixel(0, 0) and layer.get_pixel(2, 2):
        print("[PASS] New draw successful")
    else:
        print("[FAIL] New draw failed")
        return False

    # Test undo new draw
    print("\nUndo new draw...")
    if history.undo():
        print(f"After undo: {np.sum(layer.data)} pixels")
        if np.sum(layer.data) == 1 and layer.get_pixel(0, 0) and not layer.get_pixel(2, 2):
            print("[PASS] Undo new draw successful")
        else:
            print("[FAIL] Undo new draw failed")
            return False
    else:
        print("[FAIL] Undo failed")
        return False

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    return True

if __name__ == "__main__":
    success = test_undo_redo()
    sys.exit(0 if success else 1)
