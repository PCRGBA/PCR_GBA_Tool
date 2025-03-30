"""导航类"""

import time
from utils.logger import logger


class Nav:
    def __init__(self, game, templates):
        self.game = game
        self.templates = templates

    def nav_to_main(self, device_manager, sys):
        """进入游戏主界面"""
        logger.info("尝试进入游戏主界面")

        # 检测游戏是否已运行
        logger.info("检测游戏是否已运行")
        if self.game.check_game_run_status(device_manager, sys):
            logger.info("游戏已运行")

        attempts = 0
        while attempts < 6:

            # 检测是否在主界面
            self.game.click_pos((1270, 660))
            if self.game.check_main():
                logger.info("已在主界面")
                return True

            # 点击主菜单
            self.game.click_icon(self.templates.my_home_icon, max_retries=1)
            attempts += 1

        # 没有找到主菜单，重启游戏
        logger.error("没有找到主菜单，重启游戏")

        if not self.game.restart_game(device_manager):
            return False

        attempts = 0
        while attempts < 6:
            self.game.click_pos((1270, 660))
            time.sleep(2)
            # 检测是否在主界面
            if self.game.check_main():
                logger.info("成功进入主界面")
                return True
            attempts += 1

        logger.error("进入主界面失败，请联系管理员")
        return False

    def nav_to_training(self):
        """进入训练场界面"""
        logger.info("尝试进入训练场界面")

        # attempts = 0
        # # 进入训练场
        # while attempts < 6:

        #     if self.game.click_icon(self.templates.training_icon, max_retries=1):
        #         logger.info("进入训练场成功")
        #         return True

        #     attempts += 1
        #     # 点击主菜单
        #     self.game.click_pos((1164, 704))

        # 进入训练场
        # 点击主菜单
        self.game.click_pos((1164, 704))
        if self.game.click_icon(self.templates.training_icon, max_retries=1):
            logger.info("进入训练场成功")
            return True

        logger.error("进入训练场失败，请联系管理员")
        return False

    def nav_to_jjc(self):
        """进入竞技场界面"""
        logger.info("尝试进入jjc界面")

        # 点击冒险图标
        if not self.game.click_icon(self.templates.adventure_icon, max_retries=1):
            logger.error("没有找到冒险图标，进入jjc失败，请联系管理员")
            return False

        # 点击jjc
        if not self.game.click_icon(self.templates.battle_arena_icon, max_retries=1):
            logger.error("没有找到jjc图标，进入jjc失败，请联系管理员")
            return False

        logger.info("进入jjc成功")
        return True
