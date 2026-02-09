"""画布视图组件"""
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QWheelEvent, QMouseEvent, QBrush
import numpy as np
from typing import Optional

from ..core.canvas import Canvas
from ..utils.constants import MIN_ZOOM, MAX_ZOOM, ZOOM_STEP, GRID_COLOR


class CanvasView(QGraphicsView):
    """画布视图类，负责显示和交互"""

    draw_completed = pyqtSignal(object, object)  # 绘制完成信号 (old_data, new_data)
    mouse_moved = pyqtSignal(int, int)  # 鼠标移动信号 (x, y)

    def __init__(self, canvas: Canvas):
        """
        初始化画布视图

        Args:
            canvas: 画布数据模型
        """
        super().__init__()
        self.canvas = canvas
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 画布图像项
        self.canvas_item: Optional[QGraphicsPixmapItem] = None

        # 视图设置
        self.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 缩放和平移状态
        self.zoom_level = 1.0
        self.is_panning = False
        self.last_pan_point = QPointF()

        # 当前工具
        self.current_tool = None

        # 初始化画布
        self.update_canvas()

    def update_canvas(self, show_preview: bool = False) -> None:
        """
        更新画布显示

        Args:
            show_preview: 是否显示工具预览
        """
        # 合并所有可见图层
        merged_data = self.canvas.merge_visible_layers()

        # 如果有工具预览，叠加预览点
        if show_preview and self.current_tool:
            preview_points = self.current_tool.get_preview_points()
            for x, y in preview_points:
                if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                    merged_data[y, x] = True

        # 转换为 QImage
        height, width = merged_data.shape
        image = QImage(width, height, QImage.Format.Format_Mono)

        # 填充图像数据
        for y in range(height):
            for x in range(width):
                # True=黑色(0), False=白色(1)
                color = 0 if merged_data[y, x] else 1
                image.setPixel(x, y, color)

        # 绘制网格线
        if self.canvas.grid_visible:
            image = self._draw_grid(image)

        # 更新场景
        pixmap = QPixmap.fromImage(image)
        if self.canvas_item is None:
            self.canvas_item = self.scene.addPixmap(pixmap)
        else:
            self.canvas_item.setPixmap(pixmap)

        # 设置场景矩形
        self.scene.setSceneRect(0, 0, width, height)

    def _draw_grid(self, image: QImage) -> QImage:
        """
        在图像上绘制网格线

        Args:
            image: 原始图像

        Returns:
            带网格线的图像
        """
        # 转换为 RGB 格式以支持半透明网格线
        rgb_image = image.convertToFormat(QImage.Format.Format_ARGB32)

        painter = QPainter(rgb_image)
        pen = QPen(QColor(*GRID_COLOR))
        pen.setWidth(0)  # 1像素宽度
        painter.setPen(pen)

        # 绘制垂直线
        for x in range(0, self.canvas.width + 1):
            painter.drawLine(x, 0, x, self.canvas.height)

        # 绘制水平线
        for y in range(0, self.canvas.height + 1):
            painter.drawLine(0, y, self.canvas.width, y)

        painter.end()
        return rgb_image

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        鼠标滚轮事件（缩放）

        Args:
            event: 滚轮事件
        """
        # 获取滚轮增量
        delta = event.angleDelta().y()

        if delta > 0:
            # 放大
            zoom_factor = ZOOM_STEP
        else:
            # 缩小
            zoom_factor = 1.0 / ZOOM_STEP

        # 计算新的缩放级别
        new_zoom = self.zoom_level * zoom_factor

        # 限制缩放范围
        if MIN_ZOOM <= new_zoom <= MAX_ZOOM:
            self.scale(zoom_factor, zoom_factor)
            self.zoom_level = new_zoom

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        鼠标按下事件

        Args:
            event: 鼠标事件
        """
        # 中键或右键开始平移
        if event.button() == Qt.MouseButton.MiddleButton or event.button() == Qt.MouseButton.RightButton:
            self.is_panning = True
            self.last_pan_point = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        # 左键使用工具
        elif event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            scene_pos = self.mapToScene(event.pos())
            x, y = self.scene_to_canvas(scene_pos)
            self.current_tool.on_press(x, y, event.modifiers())
            self.update_canvas(show_preview=True)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        鼠标移动事件

        Args:
            event: 鼠标事件
        """
        # 发射鼠标坐标信号
        scene_pos = self.mapToScene(event.pos())
        x, y = self.scene_to_canvas(scene_pos)
        self.mouse_moved.emit(x, y)

        if self.is_panning:
            # 计算平移增量
            delta = event.pos() - self.last_pan_point
            self.last_pan_point = event.pos()

            # 移动滚动条
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
        elif self.current_tool and self.current_tool.is_drawing:
            # 工具拖拽
            self.current_tool.on_drag(x, y, event.modifiers())
            self.update_canvas(show_preview=True)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        鼠标释放事件

        Args:
            event: 鼠标事件
        """
        if self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        elif event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            # 工具释放
            scene_pos = self.mapToScene(event.pos())
            x, y = self.scene_to_canvas(scene_pos)
            self.current_tool.on_release(x, y, event.modifiers())

            # 获取绘制数据用于撤销/重做
            draw_data = self.current_tool.end_draw()
            if draw_data:
                old_data, new_data = draw_data
                self.draw_completed.emit(old_data, new_data)

            self.update_canvas(show_preview=False)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def toggle_grid(self) -> None:
        """切换网格线显示"""
        self.canvas.grid_visible = not self.canvas.grid_visible
        self.update_canvas()

    def scene_to_canvas(self, scene_pos: QPointF) -> tuple[int, int]:
        """
        将场景坐标转换为画布坐标

        Args:
            scene_pos: 场景坐标

        Returns:
            (x, y) 画布坐标
        """
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        return (x, y)

    def reset_zoom(self) -> None:
        """重置缩放"""
        self.resetTransform()
        self.zoom_level = 1.0

    def zoom_in(self) -> None:
        """放大"""
        if self.zoom_level * ZOOM_STEP <= MAX_ZOOM:
            self.scale(ZOOM_STEP, ZOOM_STEP)
            self.zoom_level *= ZOOM_STEP

    def zoom_out(self) -> None:
        """缩小"""
        if self.zoom_level / ZOOM_STEP >= MIN_ZOOM:
            self.scale(1.0 / ZOOM_STEP, 1.0 / ZOOM_STEP)
            self.zoom_level /= ZOOM_STEP

    def fit_in_view(self) -> None:
        """适应窗口大小"""
        if self.canvas_item:
            self.fitInView(self.canvas_item, Qt.AspectRatioMode.KeepAspectRatio)
            # 更新缩放级别
            transform = self.transform()
            self.zoom_level = transform.m11()

    def set_tool(self, tool) -> None:
        """
        设置当前工具

        Args:
            tool: 工具对象
        """
        self.current_tool = tool
        if tool:
            self.setCursor(tool.get_cursor())

    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        """
        绘制前景层（用于选择工具的覆盖层）

        Args:
            painter: QPainter 对象
            rect: 绘制区域
        """
        super().drawForeground(painter, rect)

        # 如果当前工具有 draw_overlay 方法，调用它
        if self.current_tool and hasattr(self.current_tool, 'draw_overlay'):
            # 保存画笔状态
            painter.save()
            # 绘制工具覆盖层
            self.current_tool.draw_overlay(painter, 1.0 / self.zoom_level)
            # 恢复画笔状态
            painter.restore()

        # 触发场景更新
        self.scene.update()
