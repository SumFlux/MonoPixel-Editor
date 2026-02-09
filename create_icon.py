#!/usr/bin/env python3
"""Convert SVG icon to ICO format for Windows"""

from PIL import Image
import io

# Since PIL doesn't support SVG directly, we'll create a simple pixel art icon
# Create a 256x256 image
size = 256
img = Image.new('RGBA', (size, size), (44, 44, 44, 255))
pixels = img.load()

# Draw pixel grid background
grid_color = (64, 64, 64, 255)
for i in range(64, 193, 16):
    for y in range(64, 192):
        pixels[i, y] = grid_color
    for x in range(64, 192):
        pixels[x, i] = grid_color

# Draw white pixels forming "M" shape
white = (255, 255, 255, 255)

# Left vertical line
for y in range(80, 177, 16):
    for dy in range(16):
        for dx in range(16):
            pixels[64 + dx, y + dy] = white

# Left diagonal
for dy in range(16):
    for dx in range(16):
        pixels[80 + dx, 96 + dy] = white
        pixels[96 + dx, 112 + dy] = white

# Middle
for dy in range(16):
    for dx in range(16):
        pixels[112 + dx, 128 + dy] = white

# Right diagonal
for dy in range(16):
    for dx in range(16):
        pixels[128 + dx, 112 + dy] = white
        pixels[144 + dx, 96 + dy] = white

# Right vertical line
for y in range(80, 177, 16):
    for dy in range(16):
        for dx in range(16):
            pixels[160 + dx, y + dy] = white

# Draw pencil icon in corner
pencil_x, pencil_y = 200, 32
# Yellow tip
for dy in range(8):
    for dx in range(8):
        pixels[pencil_x + dx, pencil_y + dy] = (255, 215, 0, 255)
# Orange body
for dy in range(8):
    for dx in range(8):
        pixels[pencil_x + dx, pencil_y + 8 + dy] = (255, 165, 0, 255)
# Brown wood
for dy in range(4):
    for dx in range(8):
        pixels[pencil_x + dx, pencil_y + 16 + dy] = (139, 69, 19, 255)
# Black tip
for dx in range(8):
    y_offset = abs(4 - dx)
    for dy in range(y_offset):
        pixels[pencil_x + dx, pencil_y + 20 + dy] = (51, 51, 51, 255)

# Save as ICO with multiple sizes
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("[OK] icon.ico created successfully!")
print("  Sizes: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16")
