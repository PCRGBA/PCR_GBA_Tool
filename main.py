"""主程序入口 - 公主连结R自动化助手"""

from core.device import DeviceManager
from core.game.jjc import JJC
from core.game.scan_inventory import ScanInventory
from utils.logger import logger
from utils.env_check import Env
from utils.game import Game
from utils.navigate import Nav
from core.templates.game_templates import GameTemplates
import time
import asyncio


def print_menu():
    print("\n===============公主连结R助手===============")
    print("1. 进入训练场")
    print("2. 重启游戏")
    # print("3. 角色识别")
    print("4. 进入竞技场防守设置")
    print("0. 退出程序")
    print("===========================================")
    print("请输入对应数字进行操作: ", end="")


async def main():
    """主程序入口"""
    try:

        env = Env()
        device_manager = DeviceManager()

        # # 连接模拟器
        # if not device_manager.connect_device():
        #     logger.error("连接模拟器失败，请检查模拟器是否正常运行")
        #     return

        # if not device_manager.check_connection():
        #     logger.error("ADB连接失败，请检查模拟器是否正常运行")
        #     return

        templates = GameTemplates()  # 游戏模板
        game = Game(templates)  # 游戏操作
        nav = Nav(game, templates)  # 导航操作
        jjc = JJC(game, nav)  # 竞技场操作
        # print("device_manager: ", device_manager.device)
        # scanner = ScanInventory(device_manager.device)  # 角色扫描

        # 获取系统信息
        sys = env.check_sys()

        # 环境检查（未来对接前端系统初始化模块）
        if not env.check_python_environment():
            return
        if not env.check_network():
            return

        # 连接模拟器
        if not device_manager.connect_device():
            logger.error("连接模拟器失败，请检查模拟器是否正常运行")
            return

        if not device_manager.check_connection():
            logger.error("ADB连接失败，请检查模拟器是否正常运行")
            return

        while True:
            print_menu()
            try:
                choice = int(input())
            except ValueError:
                logger.error("输入无效，请输入数字")
                continue

            # 游戏基础操作
            if choice == 0:
                logger.info("程序退出")
                break
            elif choice == 2:
                game.restart_game(device_manager)
                continue

            # 检查游戏运行状态，没有运行则跳过本次循环，重新输入
            if not nav.nav_to_main(device_manager, sys):
                continue

            # 功能选择
            if choice == 1:  # 训练场
                try:
                    nav.nav_to_training()
                except Exception as e:
                    logger.error(f"进入训练场失败: {str(e)}")
            # elif choice == 3:  # 角色识别
            #     try:
            #         await scanner.scan_characters()
            #         logger.info("角色识别成功")
            #     except Exception as e:
            #         logger.error(f"角色识别失败: {str(e)}")
            elif choice == 4:  # 竞技场防守设置
                try:
                    jjc.defense_setting()
                    logger.info("成功进入竞技场防守设置")
                except Exception as e:
                    logger.error(f"进入竞技场防守设置失败: {str(e)}")
            else:
                logger.error("无效的选项，请重新输入")

            time.sleep(1)

    except Exception as e:
        logger.error(f"程序异常: {str(e)}")
    finally:
        logger.info("正在清理资源...")


if __name__ == "__main__":
    asyncio.run(main())
