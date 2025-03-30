"""角色识别器"""

import time

# import logging
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from utils.avatar_detector import CharacterGridDetector
from utils.logger import logger

# logger = logging.getLogger(__name__)


class ScanInventory:
    def __init__(self, device):
        """
        初始化库存扫描器

        Args:
            device: ATX/uiautomator2 设备实例
        """
        self.device = device

        # 初始化角色检测器
        try:
            self.detector = CharacterGridDetector(device)
        except Exception as e:
            logger.error(f"初始化角色检测器失败: {e}")
            raise

        # 输出目录设置
        self.output_dir = Path(__file__).parent.parent.parent / "output" / "scans"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 滑动配置优化
        self.scroll_config = {
            "start_y": 0.75,  # 开始位置（略微调整以避免UI元素）
            "end_y": 0.25,  # 结束位置（确保不会滑过头）
            "duration": 0.8,  # 增加持续时间使滑动更稳定
            "steps": 15,  # 增加步数使滑动更平滑
        }

        # 检测重复的阈值（调整以提高准确性）
        self.duplicate_threshold = 100
        self.last_screenshot = None
        self.last_characters = set()  # 用于追踪已检测的角色

    async def _take_screenshot(self) -> Optional[np.ndarray]:
        """
        获取当前屏幕截图并直接返回图像数组
        """
        try:
            # 使用优化后的截图方法
            screen = await self.device.snapshot()
            # screen = self.device.snapshot()
            print("截图成功", screen)

            # 如果需要保存截图
            if screen is not None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = self.output_dir / f"screenshot_{timestamp}.png"
                cv2.imwrite(str(save_path), screen)

            return screen
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None

    def _is_duplicate_screen(self, current_screen: np.ndarray) -> bool:
        """
        检查当前截图是否与上一张截图重复（是否滑动到底）

        Args:
            current_screen: 当前截图的numpy数组
        """
        if self.last_screenshot is None:
            return False

        try:
            # 计算图片差异
            diff = cv2.absdiff(current_screen, self.last_screenshot)
            diff_sum = np.sum(diff)

            # 记录差异值用于调试
            logger.debug(f"Screen difference: {diff_sum}")

            return diff_sum < self.duplicate_threshold

        except Exception as e:
            logger.error(f"图片对比失败: {e}")
            return False

    async def _scroll_screen(self):
        """
        优化的屏幕滑动方法
        """
        try:
            screen_size = await self.device.window_size()
            start_y = int(screen_size[1] * self.scroll_config["start_y"])
            end_y = int(screen_size[1] * self.scroll_config["end_y"])
            center_x = screen_size[0] // 2

            await self.device.swipe(
                center_x,
                start_y,
                center_x,
                end_y,
                duration=self.scroll_config["duration"],
                steps=self.scroll_config["steps"],
            )

            # 等待滑动动画完成和界面稳定
            await self.device.sleep(1.2)

        except Exception as e:
            logger.error(f"滑动屏幕失败: {e}")
            raise

    def _process_detection_results(self, results: List[Dict]) -> List[Dict]:
        """
        处理检测结果，包括去重和排序

        Args:
            results: 原始检测结果列表
        """
        processed_results = []
        seen = set()

        for result in results:
            character = result["character"]
            if character != "Unknown" and character not in seen:
                seen.add(character)
                processed_results.append(result)

        # 按位置排序
        return sorted(processed_results, key=lambda x: x["position"])

    async def scan_characters(self, max_scans: int = 10) -> List[Dict]:
        """
        扫描并识别角色

        Args:
            max_scans: 最大扫描次数，防止无限循环
        """
        all_results = []
        scan_count = 0
        total_new_characters = 0

        logger.info("开始扫描角色库存...")

        while scan_count < max_scans:
            # 获取并检查截图
            current_screen = await self._take_screenshot()
            if current_screen is None:
                logger.error("获取截图失败，中断扫描")
                break

            # 检查是否到底
            if self._is_duplicate_screen(current_screen):
                logger.info("检测到重复画面，扫描完成")
                break

            # 更新上一张截图
            self.last_screenshot = current_screen

            # 使用检测器识别角色
            try:
                identified_results = await self.detector.detect_characters(
                    current_screen
                )

                if identified_results:
                    # 统计新发现的角色
                    new_characters = (
                        set(r["character"] for r in identified_results)
                        - self.last_characters
                    )
                    total_new_characters += len(new_characters)
                    self.last_characters.update(new_characters)

                    all_results.extend(identified_results)
                    logger.info(f"本次扫描发现 {len(new_characters)} 个新角色")
                else:
                    logger.info("当前页面未检测到角色")

            except Exception as e:
                logger.error(f"角色检测失败: {e}")
                continue

            # 检查是否需要继续滑动
            if not identified_results or len(new_characters) == 0:
                logger.info("当前页面无新角色，准备滑动到下一页")

            # 滑动到下一页
            try:
                await self._scroll_screen()
            except Exception as e:
                logger.error(f"滑动失败，中断扫描: {e}")
                break

            scan_count += 1

        # 处理最终结果
        unique_results = self._process_detection_results(all_results)

        # 打印扫描统计
        logger.info(f"扫描完成，共进行 {scan_count} 次扫描")
        logger.info(f"总计发现 {total_new_characters} 个不同角色")

        # 打印详细结果
        print("\n角色识别结果:")
        print("-" * 50)
        for result in unique_results:
            print(f"位置 #{result['position']}: {result['character']}", end="")
            if "similarity" in result and result["similarity"] > 0:
                print(f" (相似度: {result['similarity']:.2f})")
            else:
                print(" (未识别)")
        print("-" * 50)

        return unique_results


async def scan_inventory(device) -> List[Dict]:
    """
    扫描角色库存的便捷函数

    Args:
        device: ATX/uiautomator2 设备实例
    """
    try:
        scanner = ScanInventory(device)
        results = await scanner.scan_characters()
        return results
    except Exception as e:
        logger.error(f"扫描库存失败: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    # 这里需要传入实际的device实例
    asyncio.run(scan_inventory(None))
