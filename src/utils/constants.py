"""常量定义"""

# 默认画布尺寸
DEFAULT_CANVAS_WIDTH = 212
DEFAULT_CANVAS_HEIGHT = 104

# 缩放限制
MIN_ZOOM = 0.1
MAX_ZOOM = 50.0
ZOOM_STEP = 1.2

# 网格线颜色
GRID_COLOR = (200, 200, 200, 100)  # RGBA

# 像素值
PIXEL_BLACK = True
PIXEL_WHITE = False

# 工具类型
TOOL_PENCIL = "pencil"
TOOL_ERASER = "eraser"
TOOL_LINE = "line"
TOOL_RECTANGLE = "rectangle"
TOOL_CIRCLE = "circle"
TOOL_BUCKET_FILL = "bucket_fill"
TOOL_SELECT = "select"
TOOL_TEXT = "text"

# 笔触大小
BRUSH_SIZES = [1, 2, 3, 5, 7]

# 填充模式
FILL_MODE_OUTLINE = "outline"
FILL_MODE_FILLED = "filled"
FILL_MODE_BOTH = "both"
