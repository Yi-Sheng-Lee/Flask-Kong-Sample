import os
import pymysql
from time import sleep
from upgrade_package.upgrade_config import execute_subprocess, logging_config


if __name__ == '__main__':
    path = os.getcwd()
    # 建立 log 機制
    logger = logging_config()

    def set_info(info):
        logger.info(info)

    # def execute_command(command):
    #     cursor.execute(command)
    #     conn.commit()
    #     set_info(command)

    # 塞入初始化資料
    init = None
    init_cli = f"python3 {path}/upgrade_package/initial/initdata.py"
    init = execute_subprocess(init_cli)

    while True:
        if init:
            break
    print(init)
    logger.info(init)

    # 執行更新
    upgrade_cli = f"python3 {path}/upgrade_package/upgrade/mssp_upgrade.py"
    upgrade = execute_subprocess(upgrade_cli)
    while True:
        if upgrade:
            break
    print(f"upgrade: {upgrade}")
    logger.info(f"upgrade: {upgrade}")
