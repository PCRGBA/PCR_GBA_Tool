"""基础配置文件"""

# ADB路径配置
MAC_ADB_PATH = "/opt/homebrew/bin/adb"
WINDOWS_ADB_PATH = "C:/Users/wdnmd/Documents/搞机工具箱10.1.0/搞机工具箱10.1.0/adb.exe"

# 设备配置
# DEVICE_UUID = "127.0.0.1:5555" # mac设备的UUID
DEVICE_UUID = "127.0.0.1:16384"  # windows设备的UUID

# 游戏配置
GAME_ACTIVITY = "com.bilibili.priconne/.MainActivity"
PACKAGE_NAME = "com.bilibili.priconne"

# 确保这些变量可以被导出
__all__ = [
    "MAC_ADB_PATH",
    "WINDOWS_ADB_PATH",
    "DEVICE_UUID",
    "GAME_ACTIVITY",
    "PACKAGE_NAME",
]
