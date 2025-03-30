# utils/environment_check.py
"""环境检查工具"""
import requests
from utils.logger import logger
import sys
import socket
import subprocess
import platform


class Env:
    def __init__(self):
        self.check_list = [
            # 检测列表
            lambda: socket.create_connection(("www.baidu.com", 80)),
            lambda: requests.get("https://www.baidu.com"),
            lambda: subprocess.check_output("ping -n 1 www.baidu.com", shell=True),
        ]

    def check_python_environment(self):
        """检查python环境"""
        logger.info("开始检查python环境")
        python_version = sys.version
        logger.info(f"当前运行的python版本: {python_version}")

        # 检查python版本是否为3.8或以上
        if sys.version_info >= (3, 8):
            logger.info("Python版本检查通过")
            return True
        else:
            logger.error("Python版本检查失败，请使用Python 3.8或以上版本")
            return False

    def check_network(self):
        """检查网络"""
        for c in self.check_list:
            try:
                c()
                logger.info(f"网络检测通过")
                return True
            except Exception as e:
                continue

        logger.error(f"网络检测异常，请检查网络连接")
        return False

    def check_sys(self):
        """检查系统"""
        current_os = platform.system()
        return current_os
