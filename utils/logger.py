"""日志工具"""

import logging
from airtest.core.settings import Settings as ST


def setup_logger():
    """设置日志配置"""
    ST.LOG_FILE = "log.txt"
    # 设置airtest的日志级别为ERROR
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.ERROR)

    # 创建主程序logger
    app_logger = logging.getLogger("pcr_auto")
    app_logger.setLevel(logging.INFO)  # 设置总体的日志级别

    # 文件处理器 - 写入日志文件
    # file_handler = logging.FileHandler("log.txt", encoding='utf-8')
    # file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(file_formatter)
    # app_logger.addHandler(file_handler)

    # 控制台处理器 - 输出到控制台

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    app_logger.addHandler(console_handler)

    return app_logger


logger = setup_logger()
