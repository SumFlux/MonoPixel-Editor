"""主窗口"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QStatusBar, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from ..core.canvas import Canvas
from ..core.history import History, DrawCommand
from ..core.project import Project
from ..core.config import Config
from ..utils.constants import (
    DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT,
    TOOL_PENCIL, TOOL_ERASER, TOOL_LINE, TOOL_RECTANGLE,
    TOOL_CIRCLE, TOOL_BUCKET_FILL, TOOL_SELECT, TOOL_TEXT
)
from .canvas_view import CanvasView
from .toolbar import Toolbar
from .property_panel import PropertyPanel
from .layer_panel import LayerPanel
from .export_dialog import ExportDialog
from ..tools.pencil import PencilTool
from ..tools.eraser import EraserTool
from ..tools.line import LineTool
from ..tools.rectangle import RectangleTool
from ..tools.circle import CircleTool
from ..tools.bucket_fill import BucketFillTool
from ..tools.text import TextTool
from ..tools.select import SelectTool


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.setWindowTitle("MonoPixel Editor")
        self.setGeometry(100, 100, 1200, 800)

        # 创建配置管理器
        self.config = Config()

        # 创建画布
        self.canvas = Canvas(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)

        # 创建项目管理器
        self.project = Project(self.canvas)

        # 创建历史记录管理器
        self.history = History(max_size=50)

        # 创建工具实例
        self._create_tools()

        # 创建 UI
        self._create_menu_bar()
        self._create_toolbar()
        self._create_property_panel()
        self._create_layer_panel()
        self._create_central_widget()
        self._create_status_bar()

        # 连接信号
        self._connect_signals()

        # 设置默认工具
        self._set_tool(TOOL_PENCIL)

        # 标记首次显示
        self._first_show = True

    def _create_menu_bar(self) -> None:
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        new_action = QAction("新建(&N)", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._on_new)
        file_menu.addAction(new_action)

        open_action = QAction("打开(&O)...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open)
        file_menu.addAction(open_action)

        save_action = QAction("保存(&S)", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._on_save)
        file_menu.addAction(save_action)

        save_as_action = QAction("另存为(&A)...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._on_save_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        export_action = QAction("导出(&E)...", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._on_export)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")

        undo_action = QAction("撤销(&U)", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("重做(&R)", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(redo_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")

        grid_action = QAction("显示网格(&G)", self)
        grid_action.setShortcut(QKeySequence("G"))
        grid_action.setCheckable(True)
        grid_action.setChecked(True)
        grid_action.triggered.connect(self._on_toggle_grid)
        view_menu.addAction(grid_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("放大(&I)", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self._on_zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("缩小(&O)", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self._on_zoom_out)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("重置缩放(&R)", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self._on_reset_zoom)
        view_menu.addAction(reset_zoom_action)

        fit_action = QAction("适应窗口(&F)", self)
        fit_action.setShortcut(QKeySequence("Ctrl+F"))
        fit_action.triggered.connect(self._on_fit_in_view)
        view_menu.addAction(fit_action)

        # 图像菜单
        image_menu = menubar.addMenu("图像(&I)")

        canvas_size_action = QAction("画布大小(&C)...", self)
        canvas_size_action.triggered.connect(self._on_canvas_size)
        image_menu.addAction(canvas_size_action)

    def _create_tools(self) -> None:
        """创建工具实例"""
        self.tools = {
            TOOL_PENCIL: PencilTool(self.canvas),
            TOOL_ERASER: EraserTool(self.canvas),
            TOOL_LINE: LineTool(self.canvas),
            TOOL_RECTANGLE: RectangleTool(self.canvas),
            TOOL_CIRCLE: CircleTool(self.canvas),
            TOOL_BUCKET_FILL: BucketFillTool(self.canvas),
            TOOL_SELECT: SelectTool(self.canvas),
            TOOL_TEXT: TextTool(self.canvas, self.config),
        }
        self.current_tool = None

    def _create_toolbar(self) -> None:
        """创建工具栏"""
        self.toolbar = Toolbar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        # 连接工具切换信号
        self.toolbar.tool_changed.connect(self._on_tool_changed)

    def _create_property_panel(self) -> None:
        """创建属性面板"""
        self.property_panel = PropertyPanel()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.property_panel)

        # 连接属性改变信号
        self.property_panel.brush_size_changed.connect(self._on_brush_size_changed)
        self.property_panel.fill_mode_changed.connect(self._on_fill_mode_changed)

    def _create_layer_panel(self) -> None:
        """创建图层面板"""
        self.layer_panel = LayerPanel(self.canvas)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layer_panel)

    def _connect_signals(self) -> None:
        """连接信号"""
        # 画布视图信号
        self.canvas_view.draw_completed.connect(self._on_draw_completed)
        self.canvas_view.mouse_moved.connect(self._on_mouse_moved)
        self.canvas_view.zoom_changed.connect(self._on_zoom_changed)

        # 图层面板信号
        self.layer_panel.layer_changed.connect(self._on_layer_changed)
        self.layer_panel.active_layer_changed.connect(self._on_active_layer_changed)

    def _create_central_widget(self) -> None:
        """创建中央部件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 画布视图
        self.canvas_view = CanvasView(self.canvas)
        layout.addWidget(self.canvas_view, stretch=1)

    def _create_status_bar(self) -> None:
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 状态消息标签（左侧）
        self.status_message_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_message_label)

        # 添加分隔符
        separator1 = QLabel(" | ")
        self.status_bar.addWidget(separator1)

        # 坐标标签（左侧，状态消息右边）
        self.coord_label = QLabel("坐标: --, --")
        self.status_bar.addWidget(self.coord_label)

        # 添加弹性空间
        spacer = QLabel()
        spacer.setMinimumWidth(20)
        self.status_bar.addWidget(spacer, 1)  # stretch factor = 1

        # 画布尺寸标签（右侧）
        self.canvas_size_label = QLabel(
            f"画布: {self.canvas.width} x {self.canvas.height}"
        )
        self.status_bar.addPermanentWidget(self.canvas_size_label)

        # 添加分隔符
        separator2 = QLabel(" | ")
        self.status_bar.addPermanentWidget(separator2)

        # 缩放级别标签（右侧）
        self.zoom_label = QLabel("缩放: 100%")
        self.status_bar.addPermanentWidget(self.zoom_label)

    def update_status_bar(self) -> None:
        """更新状态栏"""
        self.canvas_size_label.setText(
            f"画布: {self.canvas.width} x {self.canvas.height}"
        )
        zoom_percent = int(self.canvas_view.zoom_level * 100)
        self.zoom_label.setText(f"缩放: {zoom_percent}%")

    # 菜单动作处理
    def _on_new(self) -> None:
        """新建画布"""
        from PyQt6.QtWidgets import QMessageBox, QDialog
        from .canvas_size_dialog import CanvasSizeDialog

        # 检查是否需要保存
        if self.project.is_modified():
            reply = QMessageBox.question(
                self, "保存更改",
                "当前项目已修改，是否保存？",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Yes:
                if not self._on_save():
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        # 显示画布尺寸对话框
        dialog = CanvasSizeDialog(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT, self)
        dialog.setWindowTitle("新建画布")

        if dialog.exec() == QDialog.DialogCode.Accepted:
            width, height = dialog.get_size()

            # 创建新画布
            self.canvas = Canvas(width, height)
            self.project = Project(self.canvas)
            self.history.clear()

            # 更新工具
            self._create_tools()
            self._set_tool(TOOL_PENCIL)

            # 更新 UI
            self.canvas_view.canvas = self.canvas
            self.canvas_view.update_canvas()
            self.layer_panel.canvas = self.canvas
            self.layer_panel.refresh_layers()
            self.update_status_bar()

            # 自动适应窗口
            self.canvas_view.fit_in_view()

            self.status_message_label.setText(f"已创建新画布 ({width}x{height})")

    def _on_open(self) -> None:
        """打开项目"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        # 检查是否需要保存
        if self.project.is_modified():
            reply = QMessageBox.question(
                self, "保存更改",
                "当前项目已修改，是否保存？",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Yes:
                if not self._on_save():
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        # 选择文件
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开项目", "",
            "MonoPixel Project (*.mpx);;All Files (*)"
        )

        if not file_path:
            return

        # 加载项目
        if self.project.load(file_path):
            # 清空历史记录
            self.history.clear()

            # 更新工具
            self._create_tools()
            self._set_tool(TOOL_PENCIL)

            # 更新 UI
            self.canvas_view.canvas = self.canvas
            self.canvas_view.update_canvas()
            self.layer_panel.canvas = self.canvas
            self.layer_panel.refresh_layers()
            self.update_status_bar()

            # 自动适应窗口
            self.canvas_view.fit_in_view()

            # 更新窗口标题
            self.setWindowTitle(f"MonoPixel Editor - {self.project.get_file_name()}")
            self.status_message_label.setText(f"已打开项目: {self.project.get_file_name()}")
        else:
            QMessageBox.critical(self, "错误", "打开项目失败！")

    def _on_save(self) -> bool:
        """
        保存项目

        Returns:
            是否成功保存
        """
        if self.project.file_path:
            # 已有文件路径，直接保存
            if self.project.save():
                self.setWindowTitle(f"MonoPixel Editor - {self.project.get_file_name()}")
                self.status_message_label.setText(f"已保存: {self.project.get_file_name()}")
                return True
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "错误", "保存项目失败！")
                return False
        else:
            # 没有文件路径，另存为
            return self._on_save_as()

    def _on_save_as(self) -> bool:
        """
        另存为

        Returns:
            是否成功保存
        """
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "另存为", "untitled.mpx",
            "MonoPixel Project (*.mpx);;All Files (*)"
        )

        if not file_path:
            return False

        # 保存项目
        if self.project.save(file_path):
            self.setWindowTitle(f"MonoPixel Editor - {self.project.get_file_name()}")
            self.status_message_label.setText(f"已保存: {self.project.get_file_name()}")
            return True
        else:
            QMessageBox.critical(self, "错误", "保存项目失败！")
            return False

    def _on_export(self) -> None:
        """导出"""
        dialog = ExportDialog(self.canvas, self)
        if dialog.exec():
            self.status_message_label.setText("导出成功")

    def _on_undo(self) -> None:
        """撤销"""
        if self.history.undo():
            self.canvas_view.update_canvas()
            self.layer_panel.refresh_layers()
            self.status_message_label.setText("已撤销")
        else:
            self.status_message_label.setText("无法撤销")

    def _on_redo(self) -> None:
        """重做"""
        if self.history.redo():
            self.canvas_view.update_canvas()
            self.layer_panel.refresh_layers()
            self.status_message_label.setText("已重做")
        else:
            self.status_message_label.setText("无法重做")

    def _on_toggle_grid(self) -> None:
        """切换网格线"""
        self.canvas_view.toggle_grid()
        self.status_message_label.setText(
            "网格线已" + ("显示" if self.canvas.grid_visible else "隐藏")
        )

    def _on_zoom_in(self) -> None:
        """放大"""
        self.canvas_view.zoom_in()
        self.update_status_bar()

    def _on_zoom_out(self) -> None:
        """缩小"""
        self.canvas_view.zoom_out()
        self.update_status_bar()

    def _on_reset_zoom(self) -> None:
        """重置缩放"""
        self.canvas_view.reset_zoom()
        self.update_status_bar()

    def _on_fit_in_view(self) -> None:
        """适应窗口"""
        self.canvas_view.fit_in_view()
        self.update_status_bar()

    def _on_canvas_size(self) -> None:
        """编辑画布尺寸"""
        from PyQt6.QtWidgets import QDialog
        from .canvas_size_dialog import CanvasSizeDialog

        # 显示对话框
        dialog = CanvasSizeDialog(self.canvas.width, self.canvas.height, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_width, new_height = dialog.get_size()

            # 如果尺寸没变，直接返回
            if new_width == self.canvas.width and new_height == self.canvas.height:
                return

            # 调整画布尺寸
            self.canvas.resize(new_width, new_height)

            # 更新视图
            self.canvas_view.update_canvas()
            self.layer_panel.refresh_layers()
            self.update_status_bar()

            self.status_message_label.setText(f"画布尺寸已调整为 {new_width}x{new_height}")

    def _on_tool_changed(self, tool_id: str) -> None:
        """
        工具切换事件

        Args:
            tool_id: 工具 ID
        """
        self._set_tool(tool_id)
        # 更新状态消息标签，而不是使用 showMessage
        self.status_message_label.setText(f"已切换到: {tool_id}")

    def _set_tool(self, tool_id: str) -> None:
        """
        设置当前工具

        Args:
            tool_id: 工具 ID
        """
        # 如果当前工具是文本工具，先完成编辑
        if self.current_tool and hasattr(self.current_tool, 'finalize'):
            self.current_tool.finalize()

        if tool_id in self.tools:
            self.current_tool = self.tools[tool_id]
            self.canvas_view.set_tool(self.current_tool)

            # 更新工具属性
            if tool_id in [TOOL_PENCIL, TOOL_ERASER]:
                size = self.property_panel.get_brush_size()
                if hasattr(self.current_tool, 'set_brush_size'):
                    self.current_tool.set_brush_size(size)
                elif hasattr(self.current_tool, 'set_eraser_size'):
                    self.current_tool.set_eraser_size(size)

            if tool_id in [TOOL_RECTANGLE, TOOL_CIRCLE]:
                mode = self.property_panel.get_fill_mode()
                if hasattr(self.current_tool, 'set_fill_mode'):
                    self.current_tool.set_fill_mode(mode)

    def _on_brush_size_changed(self, size: int) -> None:
        """
        笔触大小改变事件

        Args:
            size: 笔触大小
        """
        if self.current_tool:
            if hasattr(self.current_tool, 'set_brush_size'):
                self.current_tool.set_brush_size(size)
            elif hasattr(self.current_tool, 'set_eraser_size'):
                self.current_tool.set_eraser_size(size)

    def _on_fill_mode_changed(self, mode: str) -> None:
        """
        填充模式改变事件

        Args:
            mode: 填充模式
        """
        if self.current_tool and hasattr(self.current_tool, 'set_fill_mode'):
            self.current_tool.set_fill_mode(mode)

    def _on_draw_completed(self, old_data, new_data) -> None:
        """
        绘制完成事件

        Args:
            old_data: 旧的图层数据
            new_data: 新的图层数据
        """
        layer = self.canvas.get_active_layer()
        if layer and old_data is not None and new_data is not None:
            command = DrawCommand(layer, old_data, new_data)
            # 使用 add() 而不是 execute()，因为工具已经修改了图层数据
            self.history.add(command)
            self.project.mark_modified()

    def _on_layer_changed(self) -> None:
        """图层改变事件"""
        self.canvas_view.update_canvas()
        self.project.mark_modified()

    def _on_active_layer_changed(self, layer_index: int) -> None:
        """
        活动图层改变事件

        Args:
            layer_index: 新的活动图层索引
        """
        self.canvas.active_layer_index = layer_index
        self.canvas_view.update_canvas()

    def _on_mouse_moved(self, x: int, y: int) -> None:
        """
        鼠标移动事件

        Args:
            x: X 坐标
            y: Y 坐标
        """
        # 始终更新坐标显示（实时显示鼠标位置）
        self.coord_label.setText(f"坐标: {x}, {y}")

    def _on_zoom_changed(self, zoom_level: float) -> None:
        """
        缩放变化事件

        Args:
            zoom_level: 缩放级别
        """
        # 更新缩放显示
        zoom_percent = int(zoom_level * 100)
        self.zoom_label.setText(f"缩放: {zoom_percent}%")

    def closeEvent(self, event) -> None:
        """
        窗口关闭事件

        Args:
            event: 关闭事件
        """
        from PyQt6.QtWidgets import QMessageBox

        # 检查是否需要保存
        if self.project.is_modified():
            reply = QMessageBox.question(
                self, "保存更改",
                "当前项目已修改，是否保存？",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Yes:
                if not self._on_save():
                    event.ignore()
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return

        event.accept()

    def showEvent(self, event) -> None:
        """
        窗口显示事件

        Args:
            event: 显示事件
        """
        super().showEvent(event)

        # 首次显示时自动适应窗口
        if self._first_show:
            self._first_show = False
            # 使用 QTimer 延迟调用，确保窗口已完全显示
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(100, self.canvas_view.fit_in_view)

    def keyPressEvent(self, event) -> None:
        """
        键盘按下事件

        Args:
            event: 键盘事件
        """
        from PyQt6.QtCore import Qt
        from ..tools.select import SelectTool
        from ..core.history import DrawCommand

        key = event.key()

        # DEL 键删除选区
        if key == Qt.Key.Key_Delete:
            if isinstance(self.current_tool, SelectTool) and self.current_tool.has_selection():
                layer = self.canvas.get_active_layer()
                if layer and not layer.locked:
                    # 保存旧数据用于撤销
                    old_data = layer.data.copy()

                    # 删除选区
                    if self.current_tool.delete_selection():
                        # 保存新数据
                        new_data = layer.data.copy()

                        # 添加到历史记录
                        command = DrawCommand(layer, old_data, new_data)
                        self.history.add(command)

                        # 更新视图
                        self.canvas_view.update_canvas()
                        self.status_message_label.setText("已删除选区内容")
            event.accept()
            return

        # 工具切换快捷键（1-8）
        tool_map = {
            Qt.Key.Key_1: TOOL_PENCIL,
            Qt.Key.Key_2: TOOL_ERASER,
            Qt.Key.Key_3: TOOL_LINE,
            Qt.Key.Key_4: TOOL_RECTANGLE,
            Qt.Key.Key_5: TOOL_CIRCLE,
            Qt.Key.Key_6: TOOL_BUCKET_FILL,
            Qt.Key.Key_7: TOOL_SELECT,
            Qt.Key.Key_8: TOOL_TEXT,
        }

        if key in tool_map:
            self._set_tool(tool_map[key])
            self.toolbar.set_active_tool(tool_map[key])
            event.accept()
        else:
            super().keyPressEvent(event)
