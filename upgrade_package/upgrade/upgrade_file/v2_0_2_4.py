# # -*- coding: UTF-8 -*-

# 新增項目
# - 新增 自建情資權限 (PULSE_MANAGE)
# - 新增 情資資訊權限 (SENTIMENT_MANAGE)
# - 新增 操作資訊權限 (OPERATION_RECORD_MANAGE)
# - 新增 稽核權限(AUDIT_MANAGE)
# - DB operations 新增 UPLOAD 參數
# - DB login_record token VARCHAR 數值 (2000 -> 5000)


import pymysql
import os
import sys
sys.path.append(os.getcwd())
from datetime import datetime
from upgrade_package.upgrade_config import logging_config


if __name__ == '__main__':

    def set_info(info):
        logger.info(info)


    def execute_command(command):
        cursor.execute(command)
        conn.commit()
        set_info(command)


    logger = logging_config()
    set_info("======START INSERT v2.0.2.4 DATA======")

    conn = None
    cursor = None
    port = os.getenv("DB_PORT") or 5005
    db_pb = 'billows12345'
    history = None

    try:
        conn = pymysql.connect(host=os.getenv("DB_HOST") or "192.168.69.194", port=int(port),
                               user=os.getenv("DB_USER") or "msspmgr",
                               passwd=db_pb, db=os.getenv("DB_DB") or "mssp",
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `upgrade_history` WHERE `latest_version`='v2.0.2.4'")
        history = cursor.fetchone()

        # 修改 login_records.token VARCHAR value
        commit = f"ALTER TABLE `login_records` CHANGE COLUMN `token` `token` VARCHAR(5000) COLLATE 'utf8mb3_bin' NOT NULL ;"
        execute_command(commit)

        # operations 新增 UPLOAD 參數
        # 先判斷 operations 有沒有資料
        commit = "SELECT * FROM `operations` WHERE `name`='UPLOAD'"
        execute_command(commit)
        pulses = cursor.fetchall()
        conn.commit()
        if len(pulses) == 0:
            commit = "INSERT INTO `operations` (`name`) VALUES ('UPLOAD');"
            execute_command(commit)
        else:
            set_info("operation of UPLOAD is inserted")

        # 先判斷有沒有 PULSE_MANAGE 資料
        commit = "SELECT * FROM `permissions` WHERE `name`='PULSE_MANAGE'"
        execute_command(commit)
        pulses = cursor.fetchall()
        conn.commit()
        if len(pulses) == 0:
            commit = "INSERT INTO `permissions` (`name`, `enable`, `url`) VALUES ('PULSE_MANAGE', 1, '/pulse/create-manage');"
            execute_command(commit)
        else:
            set_info("permission of pulses is inserted")

        # 先判斷有沒有 SENTIMENT_MANAGE 資料
        commit = "SELECT * FROM `permissions` WHERE `name`='SENTIMENT_MANAGE'"
        execute_command(commit)
        sentiment = cursor.fetchall()
        if len(sentiment) == 0:
            commit = "INSERT INTO permissions (`name`, `enable`, `url`) VALUES ('SENTIMENT_MANAGE', 1, '/pulse/sentiment-manage');"
            execute_command(commit)
        else:
            set_info("permission of sentiment is inserted")

        # 先判斷有沒有 OPERATION_RECORD_MANAGE 資料
        commit = "SELECT * FROM `permissions` WHERE `name`='OPERATION_RECORD_MANAGE'"
        execute_command(commit)
        record = cursor.fetchall()
        if len(record) == 0:
            # 新增 操作資訊
            commit = "INSERT INTO permissions (`name`, `enable`, `url`) VALUES ('OPERATION_RECORD_MANAGE', 1, '/record/operation-manage');"
            execute_command(commit)
        else:
            set_info("permission of operation record is inserted")

        # 先判斷有沒有 AUDIT_MANAGE 資料
        commit = "SELECT * FROM `permissions` WHERE `name`='AUDIT_MANAGE'"
        execute_command(commit)
        audit = cursor.fetchall()
        if len(audit) == 0:
            # 新增 操作資訊
            commit = "INSERT INTO permissions (`name`, `enable`, `url`) VALUES ('AUDIT_MANAGE', 1, '/clause/clause-manager');"
            execute_command(commit)
        else:
            set_info("permission of clause is inserted")

        set_info("======FINISH INSERT v2.0.2.4 DATA======")

        # 更新 upgrade_history.is_upgrade
        set_info("======UPDATE upgrade_history ======")

        upgrade_history_command = "UPDATE `upgrade_history` SET `is_upgrade`='1', `update_at`='%s', `message`='success' " \
                                 "WHERE (`id`='%s');" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), history['id'])
        execute_command(upgrade_history_command)
        set_info("======UPDATE upgrade_history SUCCESS======")

        # 更新 current_version.version
        set_info("======UPDATE current_version ======")

        commit = "SELECT * FROM `current_version` WHERE `id`='1'"
        execute_command(commit)
        version = cursor.fetchall()
        conn.commit()
        if len(version) == 0:
            commit = f"INSERT INTO `current_version` (`version`, `create_at`, `update_at`) VALUES ('V2.0.2.4', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
            execute_command(commit)
        else:
            update_current_version_command = "UPDATE `current_version` SET `version`='%s', `update_at`='%s' WHERE (`id`='1');" % (
                'v2.0.2.4', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            execute_command(update_current_version_command)
        set_info("======UPDATE current_version SUCCESS======")

        print('v2.0.2.4 DONE')
    except Exception as e:
        update_current_version_command = f"UPDATE `upgrade_history` SET `is_upgrade`=0, `update_at`='%s', " \
                                         f"`message`='%s' WHERE (`id`='%s');" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e, history['id'])
        execute_command(update_current_version_command)
        print(e)
        set_info(e)

    cursor.close()
    conn.close()
    set_info("v2.0.2.4 close DB")

