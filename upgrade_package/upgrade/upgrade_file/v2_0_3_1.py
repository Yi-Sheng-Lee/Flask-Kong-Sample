# # -*- coding: UTF-8 -*-

# 新增項目
# - 新增 儀表板圖表 eps, windows_event, linux_event, statistics_ip
# - 隱藏 THREAT 儀表板
# - 更新 IOC, IOC_COUNT, PULSES, MALWARE type=mssp
# - 設定 api_tokens 內 type = isac enabled = 0
# - 隱藏 comodo 圖表
# - 新增 api url
# - 新增 web_url
# - 新增 clauseType (法規類型) SEMI-E187, 資通安全責任等級A級之公務機關應辦事項
# - 新增 clause (法規條文)


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
    set_info("======START INSERT v2.0.3.1 DATA======")

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
        cursor.execute("SELECT * FROM `upgrade_history` WHERE `latest_version`='v2.0.3.1'")
        history = cursor.fetchone()

        # 先判斷有沒有 dashboard_widgets WINDOWS_EVENT 資料
        commit = "SELECT * FROM `dashboard_widgets` WHERE `name`='WINDOWS_EVENT'"
        execute_command(commit)
        w_event = cursor.fetchall()
        conn.commit()
        if len(w_event) == 0:
            commit = "INSERT INTO `dashboard_widgets` (`uid`, `name`, `module`,`type`,`enable`) VALUES ('ad5d12a6-f249-4b4b-8386-8a4b9b1a687d','WINDOWS_EVENT','/mssp/api/1.0/dashboard/stats/windows_event','lm','1');"
            execute_command(commit)
        else:
            set_info("dashboard_widgets of WINDOWS_EVENT is inserted")

        # 先判斷有沒有 dashboard_widgets LINUX_EVENT 資料
        commit = "SELECT * FROM `dashboard_widgets` WHERE `name`='LINUX_EVENT'"
        execute_command(commit)
        l_event = cursor.fetchall()
        conn.commit()
        if len(l_event) == 0:
            commit = "INSERT INTO `dashboard_widgets` (`uid`, `name`, `module`,`type`,`enable`) VALUES ('bfce38d8-4def-4ec6-aded-ec9d545f73d0','LINUX_EVENT','/mssp/api/1.0/dashboard/stats/linux_event','lm','1');"
            execute_command(commit)
        else:
            set_info("dashboard_widgets of LINUX_EVENT is inserted")

        # 先判斷有沒有 dashboard_widgets STATISTICS_IP 資料
        commit = "SELECT * FROM `dashboard_widgets` WHERE `name`='STATISTICS_IP'"
        execute_command(commit)
        ip = cursor.fetchall()
        conn.commit()
        if len(ip) == 0:
            commit = "INSERT INTO `dashboard_widgets` (`uid`, `name`, `module`,`type`,`enable`) VALUES ('8ec92577-6e13-45bb-b2b7-2af01d5060a6','STATISTICS_IP','/mssp/api/1.0/dashboard/stats/statistics_ip','lm','1');"
            execute_command(commit)
        else:
            set_info("dashboard_widgets of STATISTICS_IP is inserted")

        # 隱藏 THREAT 儀表板
        commit = "SELECT * FROM `dashboard_widgets` WHERE `id`='7' AND `enable`='0'"
        execute_command(commit)
        threat = cursor.fetchall()
        conn.commit()
        if len(threat) == 0:
            commit = "UPDATE `dashboard_widgets` SET `enable` = '0' WHERE(`id` = '7');"
            execute_command(commit)
        else:
            set_info("dashboard_widgets of THREAT is enabled")

        # 更新 IOC, IOC_COUNT, PULSES, MALWARE type=mssp
        types = {
            3: "IOC",
            4: "IOC_COUNT",
            5: "PULSES",
            6: "MALWARE"
        }
        for k, v in types.items():
            commit = f"SELECT * FROM `dashboard_widgets` WHERE `id`='{k}' AND `type`='mssp'"
            execute_command(commit)
            item = cursor.fetchall()
            conn.commit()
            if len(item) == 0:
                commit = f"UPDATE `dashboard_widgets` SET `type` = 'mssp' WHERE(`id` = '{k}');"
                execute_command(commit)
            else:
                set_info(f"dashboard_widgets of {v} is enabled")

        # 設定 api_tokens 內 type = isac enabled = 0
        commit = "SELECT * FROM `api_tokens` WHERE `type`='isac' AND `enable`=1 "
        execute_command(commit)
        isac_list = cursor.fetchall()
        if len(isac_list) > 0:
            for item in isac_list:
                commit = f"UPDATE `api_tokens` SET `enable`= 0 WHERE(`id`='{item['id']}');"
                execute_command(commit)
        else:
            set_info(f"There is no type of isac in `api_tokens` table")

        # 隱藏 comodo 圖表
        comodo_types = ['COMODO_UNRECOGNIZED_FILE', 'COMODO_UNRECOGNIZED_HOST', 'COMODO_MALICIOUS_FILE', 'COMODO_MALICIOUS_HOST']

        for chart_name in comodo_types:
            commit = f"SELECT * FROM `dashboard_widgets` WHERE `name`='{chart_name}';"
            execute_command(commit)
            chart = cursor.fetchone()
            if chart:
                commit = f"UPDATE `dashboard_widgets` SET `enable`=0 WHERE `id`='{chart['id']}';"
                execute_command(commit)

        # 更改 /refresh api
        commit = "SELECT * FROM `api` WHERE `url`='/refresh'"
        execute_command(commit)
        refresh_api = cursor.fetchone()
        if refresh_api:
            commit = f"UPDATE `api` SET `url`='/login/refresh' WHERE (`id`='{refresh_api['id']}');"
            execute_command(commit)

        # 新增 api url (CLAUSE_PERMISSIONS)
        apis = {
            "CLAUSE_PERMISSIONS": "/cyberSecurity/clause/type/permissions",
            "CLAUSE_PERMISSION": "/cyberSecurity/clause/type/permission",
            "USER_PROFILE": "/user/profile"
        }
        for k, v in apis.items():
            commit = f"SELECT * FROM `api` WHERE `name`='{k}';"
            execute_command(commit)
            api = cursor.fetchall()
            if len(api) == 0:
                commit = f"INSERT `api` (`name`,`url`) VALUES ('{k}','{v}');"
                execute_command(commit)

        # 新增 web_url (法規類型管理)
        urls = {
            "ClauseTypeManage": "/audit/clause-type-manage"
        }
        for k, v in urls.items():
            commit = f"SELECT * FROM `web_url` WHERE `name`='{k}';"
            execute_command(commit)
            url = cursor.fetchall()
            if len(url) == 0:
                commit = f"INSERT `web_url` (`name`,`url`) VALUES ('{k}','{v}');"
                execute_command(commit)

        # 新增 CLAUSE_TYPE_MANAGE(法規權限管理)
        permissions = {
            "CLAUSE_TYPE_MANAGE": "/clause/type-manager"
        }
        for k, v in permissions.items():
            commit = f"SELECT * FROM `permissions` WHERE `name`='{k}'"
            execute_command(commit)
            permission = cursor.fetchall()
            if len(permission) == 0:
                commit = f"INSERT `permissions` (`name`, `enable`, `url`) VALUES ('{k}', 1, '{v}');"
                execute_command(commit)

        # 新增 法規類型(clauseType) SEMI E187-0122
        commit = "SELECT * FROM `clausetype` WHERE `uid`='856f8d3d-8915-469a-a45b-4d1f71844db2';"
        execute_command(commit)
        clauseType = cursor.fetchall()

        if len(clauseType) == 0:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit = f"INSERT INTO `clausetype` (`uid`,`type_name`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('856f8d3d-8915-469a-a45b-4d1f71844db2','SEMI E187-0122','ff81c0d6-e8d2-451f-a226-935cbd913541','{time}','system','4a52eeff-1124-4dea-8444-2d8e05f06fbc','{time}','system');"
            execute_command(commit)

        # 新增 法規類型(clauseType) 資通安全責任等級A級之公務機關應辦事項
        commit = "SELECT * FROM `clausetype` WHERE `type_name`='資通安全責任等級A級之公務機關應辦事項';"
        execute_command(commit)
        clauseType = cursor.fetchall()

        if len(clauseType) == 0:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit = f"INSERT INTO `clausetype` (`uid`,`type_name`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('9e7226fe-8216-4ac2-a59f-ec8c4186c8d4','資通安全責任等級A級之公務機關應辦事項','e6b725ac-06cb-4caa-87ef-f6fbe296b059','{time}','system','4d76bd7c-906b-4e7f-9d88-b1620e4a68f3','{time}','system');"
            execute_command(commit)

        # 新增法規條文 (clause) SEMI E187-0122
        commit = "SELECT * FROM `clause` WHERE `clause_type_id`='856f8d3d-8915-469a-a45b-4d1f71844db2';"
        execute_command(commit)
        clause = cursor.fetchall()

        if len(clause) == 0:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit = f"INSERT INTO `clause` (`uid`,`clause_type_id`,`clause_title_id`,`clause_title`,`clause_subtitle`,`clause_item`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('d57780f4-72f1-4649-9cd0-7793b99aded9','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'7.2 Support for Operating System','E187.00-RQ-00001-00','Equipment supplier shall not ship equipment with OS that are not supported by the OS vendor (e.g., end of life). [/RQ]','305d8b49-61c9-46c5-9d59-5c264e88f822','{time}','system','a1945fb0-58a3-42d5-ac59-41f738d3c960','{time}','system'),('ec7310fd-0aa3-4bca-8130-145ca43ebe75','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'7.2 Support for Operating System','E187.00-RQ-00002-00','Equipment suppliers shall provide the procedure to apply the patches or the security updates.It includes items to evaluate software compatibility, software package dependency, performance impact, and side-effect of applying the patches or security updates. [/RQ]','5586f1fb-828d-43a7-9fa5-f6b3aff9cc55','{time}','system','6f6ae114-588f-495b-a155-10cbf881444c','{time}','system'),('74bdb632-f12b-4601-b22b-da4d51447048','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'8.2 Network Transmission Security','E187.00-RQ-00003-00','Equipment that provides applications of web service, file transfer, and terminal service(telnet) shall support secure transmission protocols like HyperText Transfer Protocol Secure (HTTPS), Secure File Transfer Protocol (SFTP), and Secure Shell (SSH) accordingly. [/RQ]','717334cb-3c79-42e9-b87f-4ad023365ee0','{time}','system','c5ba760b-b963-4151-a5de-d219c7127f5f','{time}','system'),('5c9ac380-5e7b-405c-805a-1240ebc522ee','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'8.3 Network Configuration Management','E187.00-RQ-00004-00','Equipment supplier shall provide documentation for network configurations including network protocols/ports usage and provide maintenance instructions for changing the network configuration if supported (such as changing the network port assignment). [/RQ]','ba978909-8c43-4fb6-b0bf-dc088bb7cbc3','{time}','system','7f8eb032-7704-43da-9613-3ef1bb2c4ea0','{time}','system'),('3af770c6-7907-4d8b-9f0e-87c96fac56b5','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.2 Vulnerability Mitigation','E187.00-RQ-00005-00','Equipment suppliers shall perform vulnerability scan prior to equipment shipment and deliver a scanning report, including name and version of scanning tool, scanning scope of coverage, and scanning date, with evidence of no critical severity vulnerability according to common industrial vulnerability scoring standard. [/RQ]','bb050c22-77ad-4d80-8420-a4e901322302','{time}','system','4369a9d3-ba90-4311-8004-a368f3e4e103','{time}','system'),('041e037c-a0b7-4e0e-ab71-c73dbcc0ec18','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.3 Malware Scanning','E187.00-RQ-00006-00','Equipment suppliers shall perform malware scan prior to equipment shipment and deliver a scanning report, including name and version of scanning tool, scanning scope of coverage, and scanning date. [/RQ]','71816c72-30b0-4b0e-b76e-9a94c3c700e7','{time}','system','de2c1eba-4ae7-4aaf-8740-f1d4231281ae','{time}','system')('bdc199fa-de33-46f9-a751-01c73bc7fe64','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.4 Anti-Malware Protection','E187.00-RQ-00007-00','Equipment suppliers shall provide documentation that specifies the compatible anti-malware solutions for the fab equipment. [/RQ]','7e4bfcf9-cf6b-4941-9d4b-430070ff8fcf','{time}','system','bd90ad1f-fc9f-4505-9469-f171a7c0098d','{time}','system'),('cca24e6d-f378-479f-bf3d-766acdd0a9db','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.4 Anti-Malware Protection','E187.00-RQ-00008-00','Equipment suppliers shall provide documents regarding security hardening including:• Enable/disable input/output interfaces such as Universal Serial Bus (USB) or DVD Rewritable (DVD±RW).• Disable unused operating system utilities and services.[/RQ]','63bea039-6ead-48fb-b9a0-c7f979f041de','{time}','system','677ccdac-19c1-41fb-86bf-ace9b87fc626','{time}','system'),('6c7720dc-c305-4b43-a8c6-fe1460b2c802','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.5 Access Control Mechanism','E187.00-RQ-00009-00','Authentication mechanism(s) shall be used for operating system and equipment access control. [/RQ]','d87920ba-d683-42b7-8e43-6372ffd67abc','{time}','system','4a972d8e-c113-41e9-9c58-bec6af4f3721','{time}','system'),('59965c43-850f-4f46-b0ba-07cb39adfa6e','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.5 Access Control Mechanism','E187.00-RQ-00010-00','Equipment suppliers shall provide access rights/privileges authorization solutions to support segregation of duties and least privilege policy. [/RQ]','2f5e06c2-571b-4f7e-8d89-4b77609b42a2','{time}','system','f76b1343-7a0e-4ae4-9e06-135eeba5d087','{time}','system'),('97eafe4b-ffde-4550-b2aa-1b168bb24b0a','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'10.2 Log Requirement','E187.00-RQ-00011-00','Fab equipment shall be capable of recording and exporting system and application security event logs. [/RQ]','8d784244-119f-4f9e-9c67-e1b3284546b8','{time}','system','8ee1b8b4-8144-4fe8-89ee-928ac43e5f99','{time}','system'),('73aaa761-f59b-434a-b842-5087de68b0a5','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'10.2 Log Requirement','E187.00-RQ-00012-00','The types of event logs shall include access control, configuration changes and system errors, and the event log consists of event type, event description, user account and timestamp. [/RQ]','181a5829-94ef-4ad4-b2a1-82c6f52ce5f8','{time}','system','a757a4f1-2af0-4f99-87f7-012358d47575','{time}','system'),('c6598ac1-a73b-4ee1-b84d-af3176f73a53','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90001-00','Each party of the capabilities defined in this specification shall document compliance to E187.00 capability requirements per with Table A1-1 the following compliance codes: C – comply, NC – not comply, NA – not applicable. [/RQ]','12834b86-cd23-4cea-be02-ab7f3bd0485c','{time}','system','776cd7fb-4aba-4149-8b5e-982d2cce2319','{time}','system'),('28b7c6b2-792f-4085-a550-31d1ff458dcd','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90002-00','The NA compliance code shall be used only in the case where a requirement is conditional and the condition evaluates to render the requirement not applicable for the current implementation. [/RQ]','3c7dc65c-920d-427c-aaf5-acf9ae84bfd2','{time}','system','071667b3-0b23-4be9-9e34-df486bf68979','{time}','system'),('935231b3-749c-4b1d-900d-73a3944d249a','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90003-00','An explanation for NC shall be provided by the party. [/RQ]','33c28e38-2243-4c78-b21a-b456c7bd2ebf','{time}','system','b1dfc804-14a5-40cb-a83c-c8bf378cfb15','{time}','system');"
            execute_command(commit)

        # 新增法規條文 (clause) 資通安全責任等級A級之公務機關應辦事項
        commit = "SELECT * FROM `clause` WHERE `type_name`='資通安全責任等級A級之公務機關應辦事項';"
        execute_command(commit)
        clause = cursor.fetchall()

        if len(clause) == 0:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit = f"INSERT INTO `clause` (`uid`,`clause_type_id`,`clause_title_id`,`clause_title`,`clause_subtitle`,`clause_item`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('61959ed6-edc1-44f4-8ed8-9ab55e418fe3','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通系統分級及防護基準','資通系統分級及防護基準 ','初次受核定或等級變更後之一年內，針對自行或委外開發之資通系統，依附表九完成資通系統分級，並完成附表十之控制措施；其後應每年至少檢視一次資通系統分級妥適性。','122b5742-dcbd-4b5a-923d-17c3eb70f018','{time}','system','a6e13ac0-d0a5-4da0-b849-60f6dd9cf26f','{time}','system'),('11671c1e-ee2f-4b55-bde5-2b062f47497d','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資訊安全管理系統之導入及通過公正第三方之驗證','資訊安全管理系統之導入及通過公正第三方之驗證','初次受核定或等級變更後之二年內，全部核心資通系統導入CNS 27001資訊安全管理系統國家標準、其他具有同等或以上效果之系統或標準，或其他公務機關自行發展並經主管機關認可之標準，於三年內完成公正第三方驗證，並持續維持其驗證有效性。','3dbb6042-146e-4727-b6c1-84cae223685f','{time}','system','a5799b93-57ec-4398-a369-67254453df1b','{time}','system'),('6fa78846-585d-41d7-b71d-4f45cc17eb2e','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專責人員','資通安全專責人員','初次受核定或等級變更後之一年內，配置四人；須以專職人員配置之。','62a6ebab-41b3-49e9-b01a-25be916302a3','{time}','system','c6316708-397e-4e64-9e8b-c578a0c447b7','{time}','system'),('3dae48aa-c36a-4635-a2c6-e4648a2b0638','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'內部資通安全稽核','內部資通安全稽核','每年辦理二次。','eb422060-7c89-4857-9bdc-10383bf1ab3a','{time}','system','ab8454f2-fa4b-4060-a000-5772a2769401','{time}','system'),('7a754f60-37c6-4786-b2e3-19b931595af9','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'業務持續運作演練','業務持續運作演練','全部核心資通系統每年辦理一次。','38608f91-09c8-4b7e-a05d-80cfd6fe2600','{time}','system','7a2a2787-5c05-49ed-986e-10aad37d42b8','{time}','system'),('771ec034-c653-4182-9e83-9cf867e303ab','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資安治理成熟度評估','資安治理成熟度評估','每年辦理一次。','287db92c-1c21-429a-b5cb-693d929266b9','{time}','system','3c427654-54d2-4e8f-ada3-358ce4646df9','{time}','system'),('3700cb99-1310-44b9-88eb-38f38efd7ee2','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'安全性檢測','網站安全弱點檢測','全部核心資通系統每年辦理二次。','0a88b1fc-a517-4083-913e-a8dfe747fb9d','{time}','system','b741f611-e93a-4b96-9126-89b047f35054','{time}','system'),('a7745c90-c989-4854-88f0-eff21280b7f9','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'安全性檢測','系統滲透測試','全部核心資通系統每年辦理一次。','383b1343-1568-4d16-a185-e23ac61596f6','{time}','system','d2698316-24d2-43f5-97c9-07feca86f859','{time}','system'),('43bed624-bf8a-479b-9784-1c80996d997f','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','網路架構檢視','每年辦理一次。','22a234e0-3954-4820-b7c7-92e5a8a0d9ef','{time}','system','ed73a3c9-48ce-43fa-8693-d21cebc81015','{time}','system'),('a3c42146-3849-402a-b12a-2fbf8089f9fd','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','網路惡意活動檢視','每年辦理一次。','fea4a04e-64c4-4a59-b115-d729e613e285','{time}','system','3da5bcda-716f-4171-8b4f-a44979948cf7','{time}','system'),('81b57bb9-b51f-45e2-9eca-57acf79f647a','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','使用者端電腦惡意活動檢視','每年辦理一次。','060dc205-d8f2-46c3-994f-5bc0365d1c7e','{time}','system','c56fa6ec-c6cb-4d9e-83e9-36d37aa02452','{time}','system'),('b45e9300-868c-4c65-aa2b-2cca1c8e5a34','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','伺服器主機惡意活動檢視','每年辦理一次。','c0de9794-a958-4b22-a5c7-674b197277b0','{time}','system','9d762f84-4ecf-471d-be33-9d8aee07ad5e','{time}','system'),('add4e343-c360-4248-a6ca-8ca1f16c2ed4','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','目錄伺服器設定及防火牆連線設定檢視','每年辦理一次。','80e7fe26-14e5-41b4-ba6e-d4b85281203d','{time}','system','e810a320-23c1-4393-b64f-1957840eb973','{time}','system'),('70cc966a-75ef-433a-9736-27a7c5cd6517','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全威脅偵測管理機制','資通安全威脅偵測管理機制','初次受核定或等級變更後之一年內，完成威脅偵測機制建置，並持續維運及依主管機關指定之方式提交監控管理資料。','e8dcd84b-2f50-4d0e-8e7b-1335f42334c9','{time}','system','720b2f6b-0419-4bbb-84b1-42facc6db016','{time}','system'),('38587d52-1a66-4d0b-bd6f-00cf2870a5d2','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'政府組態基準','政府組態基準','初次受核定或等級變更後之一年內，依主管機關公告之項目，完成政府組態基準導入作業，並持續維運。','fd027a1d-e0fe-4f71-b68a-5e04322e32aa','{time}','system','09b06c01-89a4-4c22-a0cb-becc851dae67','{time}','system'),('2e2aaaf7-9b68-4f44-8f3b-1d2ff5ad5c53','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','防毒軟體','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','ed8b5dc3-1d83-482e-ac96-f565983e0c4d','{time}','system','fe787f90-7184-4b90-b5a8-a72c860305a3','{time}','system'),('b30cc9c7-d58a-48dd-ab5e-6914824eb3c7','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','網路防火牆','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','4d7a00f0-7c67-4d64-83fa-d8d2905a05b2','{time}','system','be14e698-726c-4fba-94cf-ea5c7ca69d3b','{time}','system'),('cfae0471-3c75-44c8-98b1-a28b5cb06c5a','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','具有郵件伺服器者，應備電子郵件過濾機制','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','6407b66f-b3b8-4b5f-9c62-bbaed6a2e203','{time}','system','b3881359-a2e0-4aad-99fe-b5c0ab148f2d','{time}','system'),('c0b7c185-6109-4866-ac52-cb63fbcb2ab1','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','入侵偵測及防禦機制','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','8029fa0a-e421-47dc-b389-99b05a834025','{time}','system','8ae095a3-fc46-4f44-b003-74a2dc878141','{time}','system'),('ecdbc255-2959-4a9a-ae42-66b0b14b6807','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','具有對外服務之核心資通系統者，應備應用程式防火牆','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','7f24f636-7559-4e38-9ba7-54c106bd1e8d','{time}','system','9b3beb0c-95ae-4e3d-a6af-6d0cf89fe186','{time}','system'),('d874eefc-7241-4b85-926a-01f10de0edc8','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','進階持續性威脅攻擊防禦措施','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','8a2990a3-b4bb-4cc3-8a23-939929099ef0','{time}','system','b49c35a4-401e-4b3b-ad9d-b33ddd7ac399','{time}','system'),('6004d073-f11f-4357-b504-62ee4c1a9ca6','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全教育訓練','資通安全及資訊人員','每年至少四名人員各接受十二小時以上之資通安全專業課程訓練或資通安全職能訓練。','659103a2-c10d-42b8-a2b3-dd34ecb199b2','{time}','system','45e911a9-9eec-487b-9dbc-3db2e9cd7304','{time}','system'),('c01fb734-e041-4380-8bc3-bfada84f21c5','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全教育訓練','一般使用者及主管','每人每年接受三小時以上之一般資通安全教育訓練。','55b727c3-d673-40f6-a3ff-1392f266cf96','{time}','system','14a5c720-19d3-40b3-9cfb-f4ffbcc720ee','{time}','system'),('02d09ed9-b3c6-438f-8538-86f020c3b3c4','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專業證照及職能訓練證書','資通安全專業證照','初次受核定或等級變更後之一年內，資資通安全專業證照及職能訓練證書資通安全專業證照資通安全職能評量證書通安全專職人員總計應持有四張以上並持續維持證照之有效性。','24eab8f1-e527-46d8-8cbd-a6f76cfe18c9','{time}','system','b87a20ad-8fa5-439e-8c1a-ff2d427b30d4','{time}','system'),('28b98dbf-8ee9-49e9-88ed-1273aa269e59','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專業證照及職能訓練證書','資通安全職能評量證書','初次受核定或等級變更後之一年內，資通安全專職人員總計應持有四張以上並持續維持證書之有效性','2e16c4c9-2fcd-4638-842e-3e44061ef0fb','{time}','system','9fb72456-078a-4f88-991b-99cc0195a991','{time}','system');"
            execute_command(commit)

        set_info("======FINISH INSERT v2.0.3.1 DATA======")

        # 更新 upgrade_history.is_upgrade
        set_info("======UPDATE upgrade_history ======")

        upgrade_history_command = f"UPDATE `upgrade_history` SET `is_upgrade`='1',`update_at`='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', `message`='success' WHERE (`id`='{history['id']}');"
        execute_command(upgrade_history_command)
        set_info("======UPDATE upgrade_history SUCCESS======")

        # 更新 current_version.version
        set_info("======UPDATE current_version ======")

        commit = "SELECT * FROM `current_version` WHERE `id`='1'"
        execute_command(commit)
        version = cursor.fetchall()
        conn.commit()
        if len(version) == 0:
            commit = f"INSERT INTO `current_version` (`version`, `create_at`, `update_at`) VALUES ('V2.0.3.1', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
            execute_command(commit)
        else:
            update_current_version_command = f"UPDATE `current_version` SET `version`='v2.0.3.1',`update_at`='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE (`id`='1');"
            execute_command(update_current_version_command)
        set_info("======UPDATE current_version SUCCESS======")

        print('v2.0.3.1 DONE')
    except Exception as e:
        update_current_version_command = f"UPDATE `upgrade_history` SET `is_upgrade`=0,`update_at`='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',`message`='{e}' WHERE (`id`='{history['id']}');"
        execute_command(update_current_version_command)
        print(e)
        set_info(e)

    cursor.close()
    conn.close()
    set_info("v2.0.3.1 close DB")

