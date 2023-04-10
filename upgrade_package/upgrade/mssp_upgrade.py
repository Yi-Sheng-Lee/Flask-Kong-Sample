# -*- coding: utf-8 -*-

import pymysql
import os
import sys
from datetime import datetime
from time import sleep
sys.path.append(os.getcwd())

from mssp_upgrade_config import VERSION as mssp_version
from upgrade_package.upgrade_config import execute_subprocess, logging_config

mssp_version_list = mssp_version

if __name__ == '__main__':
    logger = logging_config()
    path = os.getcwd()


    def set_info(info):
        logger.info(info)


    def execute_command(command):
        cursor.execute(command)
        conn.commit()
        set_info(command)


    def run_upgrade():
        while True:
            try:
                cursor.execute("SELECT * FROM mssp.upgrade_history WHERE `is_upgrade` = '0'")
                conn.commit()
                upgrade_data = cursor.fetchall()
                conn.commit()
                sleep(1)
                if len(upgrade_data) > 0:
                    next_version = upgrade_data[0]["latest_version"]
                    (ps) = execute_subprocess(f"python3 {path}/upgrade_package/upgrade/upgrade_file/{next_version.replace('.', '_')}.py")
                    sleep(1)
                    if ps != f"{next_version} DONE":
                        logger.error(ps)
                    else:
                        set_info(f"{next_version} UPDATE SUCCESS")
                else:
                    print("UPGRADE DONE")
                    break

                sleep(1)

            except Exception as e:
                print(e)
                set_info(e)
                break
        print("DONE")

    conn = None
    cursor = None
    port = os.getenv("DB_PORT") or "5005"
    db_pb = 'billows12345'
    version = os.getenv("VERSION") or "v2.0.2.4"

    try:
        conn = pymysql.connect(host=os.getenv("DB_HOST") or "192.168.69.194", port=int(port),
                               user=os.getenv("DB_USER") or "msspmgr",
                               passwd=db_pb, db=os.getenv("DB_DB") or "mssp",
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 先判斷有沒有需要更新的
        execute_command("SELECT * FROM `upgrade_history` WHERE (`is_upgrade`=0)")
        need_update = cursor.fetchall()
        if len(need_update) == 0:
            # 取得 current_version 資料
            execute_command("SELECT * FROM `current_version`;")
            current_version_data = cursor.fetchall()

            # 取得現在版本，若是未 docker 化的，版本號會直接為 v2.0.2.4
            current_version = version if len(current_version_data) == 0 else current_version_data[0]["version"]

            # 找尋 mssp_version_list["version"] == current_version 的 key
            index = next((index for (index, d) in enumerate(mssp_version_list) if d["version"] == current_version), None)
            # 刪除 0 ~ index 的版本，剩下的版本即為須更新版本
            del mssp_version_list[0:index + 1]

            lock_upgrade_history_command = "LOCK TABLES `upgrade_history` WRITE;"
            lock_current_version_command = "LOCK TABLES `current_version` WRITE;"
            close_command = "UNLOCK TABLES;"

            if len(mssp_version_list) > 0:
                upgrade_history = []
                if version == "v2.0.2.4":
                    upgrade_history.append(f"('x', 'v2.0.2.4', 0)")
                for i in range(len(mssp_version_list)):
                    if i == 0:
                        upgrade_history.append(f"('{current_version}', '{mssp_version_list[i]['version']}', 0)")
                    else:
                        upgrade_history.append(
                            f"('{mssp_version_list[i - 1]['version']}', '{mssp_version_list[i]['version']}', 0)")
                upgrade_history = ",".join(upgrade_history)
                set_info(f"upgrade_history: {str(upgrade_history)}")
                # 把更新資料寫入資料庫
                execute_command("SELECT * FROM `upgrade_history`;")
                upgrade_history_command = f"INSERT INTO `upgrade_history` (`previous_version`,`latest_version`,`is_upgrade`) VALUES {upgrade_history};"

                execute_command(lock_upgrade_history_command)
                execute_command(upgrade_history_command)
                execute_command(close_command)

                run_upgrade()
            # 因為 v2.0.2.4 版之前未 docker 化，故須獨立出來執行
            elif current_version == "v2.0.2.4":
                execute_command("SELECT * FROM `upgrade_history` WHERE `latest_version`='v2.0.2.4';")
                check_v2024 = cursor.fetchall()
                conn.commit()
                if len(check_v2024) == 0:
                    # execute_command(lock_current_version_command)
                    # execute_command(f"INSERT INTO `current_version` (`version`,`create_at`,`update_at`) VALUES ('v2.0.2.4', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');")
                    # execute_command(close_command)

                    execute_command(lock_upgrade_history_command)
                    execute_command(f"INSERT INTO `upgrade_history` (`previous_version`,`latest_version`,`is_upgrade`) VALUES ('x','v2.0.2.4',0);")
                    execute_command(close_command)
                    run_upgrade()
                else:
                    print("UNNECESSARY UPGRADE")
            else:
                print("UNNECESSARY UPGRADE")
        else:
            run_upgrade()
    except Exception as e:
        set_info(e)
        print(e)

    conn.close()
    cursor.close()
