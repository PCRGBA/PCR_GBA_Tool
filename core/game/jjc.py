"""竞技场相关功能"""

from pathlib import Path
from airtest.core.api import Template, touch, exists
from utils.logger import logger


class JJC:
    def __init__(self, game, nav):
        self.game = game
        self.nav = nav

    # 防守设置
    def defense_setting(self):
        """进入防守设定页面"""
        # 进入竞技场页面
        self.nav.nav_to_jjc()

        logger.info("进入防守设定页面...")
        # 点击防守设定图标
        self.game.click_icon(self.game.templates.defense_setting_icon)
