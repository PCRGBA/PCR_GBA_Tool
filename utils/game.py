from utils.logger import logger
from core.templates import GameTemplates
import time
from airtest.core.api import touch, exists, swipe
from setting import PACKAGE_NAME


class Game:
    def __init__(self, templates):
        self.GAME_PACKAGE = PACKAGE_NAME
        self.templates = templates  # 基础图标

    def restart_game(self, device_manager):
        """重启游戏"""
        logger.info("准备重启游戏")
        try:
            device_manager.device.shell(f"am force-stop {self.GAME_PACKAGE}")
            logger.info("游戏已停止")
            time.sleep(2)
            if self.click_icon(icon=self.templates.app_icon):
                logger.info("游戏重启成功，等待启动界面")
                time.sleep(15)
                return True
            else:
                logger.error("游戏启动失败")
                return False
        except Exception as e:
            logger.error(f"重启游戏失败: {str(e)}")
            return False

    def check_main(self):
        """检查主界面"""
        try:
            if (
                exists(self.templates.my_home_select_icon)
                and not exists(self.templates.close_icon)
                and not exists(self.templates.setup_main_menu_icon)
            ):
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"检查主界面时出错: {str(e)}")
            return False

    def ensure_game_running(self, device_manager, sys):
        """检查并确保游戏运行"""
        if not device_manager.check_game_activity(sys):
            logger.info("游戏未启动")
            self.restart_game(device_manager)
            return True
        logger.info("游戏已启动")
        return True

    def click_icon(self, icon, max_retries=3):
        """点击图标"""
        retry_count = 0
        while retry_count < max_retries:
            if exists(icon):
                touch(icon)
                time.sleep(0.5)
                return True
            logger.info(f"未找到图标")
            retry_count += 1
        return False

    @staticmethod
    def find_icon(icon):
        """查找图标"""
        if exists(icon):
            pos = exists(icon)
            logger.info(f"找到图标，坐标：{pos}")
            return pos
        else:
            logger.info(f"未找到图标")
            return None

    @staticmethod
    def check_game_run_status(device_manager, sys):
        """检查游戏运行状态"""
        if device_manager.check_game_activity(sys):
            return True
        return False

    @staticmethod
    def click_pos(pos):
        """点击坐标"""
        logger.info(f"点击坐标：{pos}")
        touch(pos)
        time.sleep(0.5)

    @staticmethod
    def swipe_screen(start_pos, end_pos):
        """滑动屏幕"""
        swipe(start_pos, end_pos)
        time.sleep(0.5)
