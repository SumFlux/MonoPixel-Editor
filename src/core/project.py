"""项目管理"""
import json
import base64
import numpy as np
from pathlib import Path
from typing import Optional
import logging

from .canvas import Canvas
from .layer import Layer
from .text_object import TextObject

logger = logging.getLogger(__name__)


class Project:
    """项目管理类"""

    VERSION = "1.0"

    def __init__(self, canvas: Canvas, file_path: Optional[str] = None):
        """
        初始化项目

        Args:
            canvas: 画布对象
            file_path: 项目文件路径
        """
        self.canvas = canvas
        self.file_path = file_path
        self.modified = False

    def save(self, file_path: Optional[str] = None) -> bool:
        """
        保存项目

        Args:
            file_path: 保存路径，如果为 None 则使用当前路径

        Returns:
            是否成功保存
        """
        if file_path:
            self.file_path = file_path

        if not self.file_path:
            return False

        try:
            # 构建项目数据
            project_data = {
                "version": self.VERSION,
                "canvas": {
                    "width": self.canvas.width,
                    "height": self.canvas.height,
                    "grid_visible": self.canvas.grid_visible,
                    "active_layer_index": self.canvas.active_layer_index
                },
                "layers": []
            }

            # 保存所有图层
            for layer in self.canvas.layers:
                layer_data = {
                    "name": layer.name,
                    "visible": layer.visible,
                    "locked": layer.locked,
                    "width": layer.width,
                    "height": layer.height,
                    "layer_type": layer.layer_type
                }

                # 根据图层类型保存数据
                if layer.layer_type == "bitmap" and layer.data is not None:
                    layer_data["data"] = self._encode_layer_data(layer.data)
                elif layer.layer_type == "text" and layer.text_object:
                    layer_data["text_object"] = layer.text_object.to_dict()

                project_data["layers"].append(layer_data)

            # 写入文件
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)

            self.modified = False
            return True

        except PermissionError as e:
            logger.error(f"保存项目失败 - 权限不足: {e}")
            return False
        except IOError as e:
            logger.error(f"保存项目失败 - IO错误: {e}")
            return False
        except Exception as e:
            logger.error(f"保存项目失败 - 未知错误: {e}")
            return False

    def load(self, file_path: str) -> bool:
        """
        加载项目

        Args:
            file_path: 项目文件路径

        Returns:
            是否成功加载
        """
        try:
            # 读取文件
            with open(file_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)

        except FileNotFoundError:
            logger.error(f"加载项目失败 - 文件不存在: {file_path}")
            return False
        except PermissionError:
            logger.error(f"加载项目失败 - 权限不足: {file_path}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"加载项目失败 - JSON 解析错误: {e}")
            return False
        except IOError as e:
            logger.error(f"加载项目失败 - IO错误: {e}")
            return False

        try:
            # 验证数据结构
            if not isinstance(project_data, dict):
                logger.error("加载项目失败 - 根对象不是字典")
                return False

            if "canvas" not in project_data:
                logger.error("加载项目失败 - 缺少 canvas 字段")
                return False

            if "layers" not in project_data:
                logger.error("加载项目失败 - 缺少 layers 字段")
                return False

            # 检查版本
            version = project_data.get("version", "1.0")
            if version != self.VERSION:
                logger.warning(f"项目版本不匹配 (文件: {version}, 当前: {self.VERSION})")

            # 加载画布设置
            canvas_data = project_data["canvas"]
            if not isinstance(canvas_data, dict):
                logger.error("加载项目失败 - canvas 字段不是字典")
                return False

            # 验证画布尺寸
            width = canvas_data.get("width")
            height = canvas_data.get("height")
            if not isinstance(width, int) or not isinstance(height, int):
                logger.error("加载项目失败 - 画布尺寸类型错误")
                return False
            if width <= 0 or height <= 0 or width > 10000 or height > 10000:
                logger.error(f"加载项目失败 - 画布尺寸超出范围: {width}x{height}")
                return False

            # 重新创建画布
            self.canvas.width = width
            self.canvas.height = height
            self.canvas.grid_visible = canvas_data.get("grid_visible", True)
            self.canvas.layers.clear()

            # 验证图层数据
            layers_data = project_data["layers"]
            if not isinstance(layers_data, list):
                logger.error("加载项目失败 - layers 字段不是列表")
                return False

            # 加载所有图层
            for i, layer_data in enumerate(layers_data):
                if not isinstance(layer_data, dict):
                    logger.warning(f"跳过图层 {i} - 不是字典")
                    continue

                # 验证必需字段
                if "width" not in layer_data or "height" not in layer_data or "name" not in layer_data:
                    logger.warning(f"跳过图层 {i} - 缺少必需字段")
                    continue

                # 获取图层类型（向后兼容：默认为 bitmap）
                layer_type = layer_data.get("layer_type", "bitmap")

                try:
                    layer = Layer(
                        layer_data["width"],
                        layer_data["height"],
                        layer_data["name"],
                        layer_type
                    )
                    layer.visible = layer_data.get("visible", True)
                    layer.locked = layer_data.get("locked", False)

                    # 根据图层类型加载数据
                    if layer_type == "bitmap":
                        # 位图图层：解码位图数据
                        if "data" in layer_data:
                            layer.data = self._decode_layer_data(
                                layer_data["data"],
                                layer_data["width"],
                                layer_data["height"]
                            )
                    elif layer_type == "text":
                        # 文本图层：加载文本对象
                        if "text_object" in layer_data:
                            layer.text_object = TextObject.from_dict(layer_data["text_object"])

                    self.canvas.layers.append(layer)
                except Exception as e:
                    logger.warning(f"跳过图层 {i} - 加载失败: {e}")
                    continue

            # 确保至少有一个图层
            if len(self.canvas.layers) == 0:
                logger.error("加载项目失败 - 没有有效的图层")
                return False

            # 设置活动图层
            self.canvas.active_layer_index = canvas_data.get("active_layer_index", 0)

            # 确保活动图层索引有效
            if self.canvas.active_layer_index >= len(self.canvas.layers):
                self.canvas.active_layer_index = len(self.canvas.layers) - 1

            self.file_path = file_path
            self.modified = False
            logger.info(f"成功加载项目: {file_path}")
            return True

        except Exception as e:
            logger.error(f"加载项目失败 - 未知错误: {e}")
            return False

    @staticmethod
    def _encode_layer_data(data: np.ndarray) -> str:
        """
        编码图层数据为 Base64

        Args:
            data: 图层数据

        Returns:
            Base64 编码的字符串
        """
        # 将布尔数组转换为字节
        packed = np.packbits(data.flatten())
        # Base64 编码
        encoded = base64.b64encode(packed).decode('ascii')
        return encoded

    @staticmethod
    def _decode_layer_data(encoded: str, width: int, height: int) -> np.ndarray:
        """
        解码 Base64 图层数据

        Args:
            encoded: Base64 编码的字符串
            width: 宽度
            height: 高度

        Returns:
            图层数据
        """
        # Base64 解码
        packed = base64.b64decode(encoded.encode('ascii'))
        # 转换为 uint8 数组
        packed_array = np.frombuffer(packed, dtype=np.uint8)
        # 解包为布尔数组
        unpacked = np.unpackbits(packed_array)
        # 裁剪到正确大小并重塑
        data = unpacked[:width * height].reshape((height, width)).astype(bool)
        return data

    def get_file_name(self) -> str:
        """
        获取文件名（不含路径）

        Returns:
            文件名
        """
        if self.file_path:
            return Path(self.file_path).name
        return "未命名"

    def mark_modified(self) -> None:
        """标记项目已修改"""
        self.modified = True

    def is_modified(self) -> bool:
        """
        检查项目是否已修改

        Returns:
            是否已修改
        """
        return self.modified
