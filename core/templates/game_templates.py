from airtest.core.api import Template
from pathlib import Path


class GameTemplates:
    """游戏模板管理类"""

    def __init__(self):
        # 设置基础图片路径
        self.button_path = Path("static/images/button")

    @property
    def app_icon(self):
        """游戏图标"""
        return Template(str(self.button_path / "游戏图标.png"))

    @property
    def training_icon(self):
        """训练场图标"""
        return Template(str(self.button_path / "大家的训练场.png"))

    @property
    def adventure_icon(self):
        """冒险图标"""
        return Template(str(self.button_path / "冒险.png"))

    @property
    def main_menu_icon(self):
        """主菜单图标"""
        return Template(str(self.button_path / "主菜单.png"))

    @property
    def swipe_long(self):
        """长蓝条"""
        return Template(str(self.button_path / "长蓝条.png"))

    @property
    def swipe_short(self):
        """短蓝条"""
        return Template(str(self.button_path / "短蓝条.png"))

    @property
    def my_home_icon(self):
        """我的主页图标"""
        return Template(str(self.button_path / "我的主页.png"))

    @property
    def battle_arena_icon(self):
        """战斗竞技场图标"""
        return Template(str(self.button_path / "战斗竞技场.png"))

    @property
    def defense_setting_icon(self):
        """防守设定图标"""
        return Template(str(self.button_path / "防守设定.png"))

    @property
    def my_home_select_icon(self):
        """我的主页选中图标"""
        return Template(str(self.button_path / "我的主页_select.png"))

    @property
    def close_icon(self):
        """关闭图标"""
        return Template(str(self.button_path / "关闭.png"))

    @property
    def setup_main_menu_icon(self):
        """启动主菜单图标"""
        return Template(str(self.button_path / "启动主菜单.png"))