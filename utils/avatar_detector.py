"""角色识别工具"""

import os
import cv2
import numpy as np
# import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from tqdm import tqdm
from utils.logger import logger

# # 配置日志
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)


class CharacterGridDetector:
    def __init__(self, character_data: Dict = None):
        """
        初始化检测器

        Args:
            character_data: 角色数据字典
        """
        self.character_data = character_data or {}

        # 颜色范围配置
        self.color_ranges = [
            (np.array([0, 40, 50]), np.array([30, 255, 255])),  # 橙色范围
            (np.array([15, 40, 50]), np.array([40, 255, 255])),  # 黄色范围
        ]

        # 形态学操作参数
        self.morph_kernel = np.ones((5, 5), np.uint8)
        self.close_iterations = 2
        self.open_iterations = 1

        # 检测参数
        self.min_area = 3000
        self.max_area = 60000
        self.aspect_ratio_range = (0.6, 1.4)
        self.similarity_threshold = 0.3

    def _normalize_path(self, path: Union[str, Path]) -> Path:
        """标准化路径"""
        return Path(str(path).replace("\\", os.sep)).resolve()

    def _ensure_path(self, path: Union[str, Path]) -> Path:
        """确保路径存在且格式正确"""
        path = self._normalize_path(path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        return path

    def _load_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """安全地加载图片"""
        path = self._normalize_path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        img = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"无法解码图片: {path}")
        return img

    def _save_image(self, image: np.ndarray, save_path: Union[str, Path]) -> bool:
        """安全地保存图片"""
        save_path = self._normalize_path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        return cv2.imencode(save_path.suffix, image)[1].tofile(str(save_path))

    def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """图像比较方法"""
        try:
            img1 = cv2.resize(img1, (64, 64))
            img2 = cv2.resize(img2, (64, 64))
            hist_score = cv2.compareHist(
                cv2.calcHist([img1], [0], None, [256], [0, 256]),
                cv2.calcHist([img2], [0], None, [256], [0, 256]),
                cv2.HISTCMP_CORREL,
            )
            return hist_score
        except Exception as e:
            logger.error(f"图像比较失败: {e}")
            return 0.0

    def detect_character_boxes(
        self, image_path: Union[str, Path], output_path: Union[str, Path]
    ) -> List[Dict]:
        """检测角色框"""
        img = self._load_image(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in self.color_ranges:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        results = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if self.min_area < w * h < self.max_area:
                results.append({"box": (x, y, w, h)})
        return results


def capture_screenshot(save_path: Union[str, Path]) -> None:
    """在模拟器中截屏"""
    try:
        logger.info("正在模拟器中截屏...")
        os.system(f"adb exec-out screencap -p > {save_path}")
        logger.info(f"截图已保存到: {save_path}")
    except Exception as e:
        logger.error(f"截图失败: {e}")


def main():
    base_dir = Path(__file__).parent
    static_dir = base_dir / "static/images/avatar"
    db_path = base_dir / "static/pcr_db.json"
    screenshot_path = base_dir / "screenshot.png"
    output_path = base_dir / "detected_results.png"

    # 加载角色数据库
    if not db_path.exists():
        logger.error("角色数据库文件不存在！")
        return
    with open(db_path, "r", encoding="utf-8") as f:
        character_data = json.load(f)
        for char_id, char_info in character_data.items():
            if "image_path" in char_info:
                char_info["image_path"] = str(static_dir / char_info["image_path"])

    # 截图
    capture_screenshot(screenshot_path)

    # 检测
    detector = CharacterGridDetector(character_data)
    results = detector.detect_character_boxes(screenshot_path, output_path)

    if results:
        logger.info("检测完成！角色框信息如下：")
        for res in results:
            logger.info(f"框位置: {res['box']}")
    else:
        logger.warning("未检测到任何角色！")


if __name__ == "__main__":
    main()
