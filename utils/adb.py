# utils/adb.py
"""ADB工具类"""
import subprocess
import platform
from setting import MAC_ADB_PATH, WINDOWS_ADB_PATH, DEVICE_UUID
from utils.logger import logger
from utils.env_check import Env


class ADBTool:
    def __init__(self):
        self.env = Env()
        self.adb_path = self._get_adb_path()
        self.current_os = None

    def _get_adb_path(self):
        """获取ADB路径"""
        self.current_os = self.env.check_sys()  # 检查系统环境
        logger.info(f"当前操作系统: {self.current_os}")

        if self.current_os == "Windows":
            return WINDOWS_ADB_PATH
        elif self.current_os == "Darwin":  # platform.system() 在 Mac 上返回 "Darwin"
            return MAC_ADB_PATH
        else:
            return MAC_ADB_PATH  # 默认返回 MAC 路径

    def run_command(self, command):
        """执行ADB命令"""
        try:
            full_command = f'"{self.adb_path}" {command}'
            logger.info(f"执行ADB命令: {full_command}")

            # '|'用来连接多个命令
            if "|" in command:
                # 多个命令需要使用Popen来执行复杂命令
                process = subprocess.Popen(
                    full_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output, error = process.communicate()
                if error:
                    logger.warning(f"命令执行产生警告: {error}")
                return output
            else:
                result = subprocess.check_output(
                    full_command, shell=True, text=True, stderr=subprocess.PIPE
                )
                return result
        except subprocess.CalledProcessError as e:
            logger.error(f"ADB命令执行失败: {str(e)}")
            return None
