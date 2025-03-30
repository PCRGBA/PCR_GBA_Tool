# core/device.py
"""设备连接管理"""
from airtest.core.api import init_device
from utils.adb import ADBTool
from utils.logger import logger
from setting import DEVICE_UUID, PACKAGE_NAME, GAME_ACTIVITY


class DeviceManager:
    def __init__(self):
        self.adb_tool = ADBTool()
        self.device = None
        self.device_uuid = DEVICE_UUID
        self.package_name = PACKAGE_NAME
        self.game_activity = GAME_ACTIVITY

    def connect_device(self):
        """连接模拟器"""
        try:
            self.device = init_device(platform="android", uuid=self.device_uuid)
            logger.info(f"设备连接成功: {self.device}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            return False

    def check_connection(self):
        """检查ADB连接状态"""
        try:
            result = self.adb_tool.run_command(f"-s {self.device_uuid} devices")
            logger.info(f"ADB连接状态: {result}")
            return self.device_uuid in result and "device" in result
        except:
            return False

    def check_game_activity(self, sys):
        """检测游戏是否在运行"""
        if sys == "Darwin":
            result = self.adb_tool.run_command(
                f'-s {self.device_uuid} shell dumpsys window | grep "mFocusedApp"'
            )
        else:
            # Windows
            result = self.adb_tool.run_command(
                f'-s {self.device_uuid} shell dumpsys window | findstr "mFocusedApp"'
            )
        return bool(result and self.game_activity in result)

    def close_game(self, sys):
        """关闭游戏"""
        try:
            if self.check_game_activity(sys):
                self.adb_tool.run_command(
                    f"-s {self.device_uuid} shell am force-stop {self.package_name}"
                )
                logger.info("关闭游戏成功")
                return True
            return True
        except Exception as e:
            logger.error(f"关闭游戏失败: {str(e)}")
            return False
