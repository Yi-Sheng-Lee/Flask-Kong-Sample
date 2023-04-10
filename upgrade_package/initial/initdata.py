# -*- coding: utf-8 -*-
from locale import currency
import pymysql
import os
import sys

sys.path.append(os.getcwd())

from datetime import datetime
from upgrade_package.upgrade_config import logging_config

if __name__ == '__main__':
    logger = logging_config()


    def set_info(info):
        logger.info(info)


    def execute_command(command):
        cursor.execute(command)
        set_info(command)


    conn = None
    cursor = None
    port = os.getenv("DB_PORT") or "5005"
    host = os.getenv("DB_HOST") or "192.168.69.194"
    db_pb = 'billows12345'

    try:
        conn = pymysql.connect(host=host, port=int(port),
                               user=os.getenv("DB_USER") or "msspmgr",
                               passwd=db_pb, db=os.getenv("DB_DB") or "mssp",
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        set_info("CONNECT SUCCESS")

        execute_command(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'mssp' AND TABLE_NAME = 'alembic_version';")

        items = cursor.fetchall()

        ##判斷是否經過 migration 針對每個schema 逐步寫入預設資料
        if len(items) == 1:
            set_info("======START SETTING DEFAULT DATA======")
            close_command = "UNLOCK TABLES;"

            # mssp.city
            execute_command("SELECT * FROM mssp.city;")
            citys = cursor.fetchall()
            if len(citys) == 0:
                set_info("======START SETTING city DATA======")
                lock_city_command = "LOCK TABLES `city` WRITE;"

                city_command = "INSERT INTO `city` VALUES (1,'TW','LJF','連江縣'),(2,'TW','JME','金門縣'),(3,'TW','ILA','宜蘭縣'),(4,'TW','HSQ','新竹縣'),(5,'TW','MIA','苗栗縣'),(6,'TW','CHA','彰化縣'),(7,'TW','NAN','南投縣'),(8,'TW','YUN','雲林縣'),(9,'TW','CYQ','嘉義縣'),(10,'TW','PIF','屏東縣'),(11,'TW','TTT','臺東縣'),(12,'TW','HUA','花蓮縣'),(13,'TW','PEN','澎湖縣'),(14,'TW','KEE','基隆市'),(15,'TW','HSZ','新竹市'),(16,'TW','CYI','嘉義市'),(17,'TW','TPE','臺北市'),(18,'TW','KHH','高雄市'),(19,'TW','TPQ','新北市'),(20,'TW','TXG','臺中市'),(21,'TW','TNN','臺南市'),(22,'TW','TAO','桃園市');"
                execute_command(lock_city_command)
                execute_command(city_command)
                execute_command(close_command)
                set_info("======END SETTING city DATA======")
            else:
                set_info(f"mssp.city length: {len(citys)}")

            # mssp.companies
            execute_command("SELECT * FROM mssp.companies;")
            companies = cursor.fetchall()

            if len(companies) == 0:
                lock_comanies_command = "LOCK TABLES `companies` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                companies_command = f"INSERT INTO `companies` VALUES (1,'7cc7bccb-1295-4fb7-a743-00f9860c6ed3',1,'預設管理公司','聯絡人','contact@billows.com.tw','022345678','12345678','TW','TPE','104','請輸入地址','系統預設管理公司',0,1,'system','{time}','Admin','{time}');"
                execute_command(lock_comanies_command)
                execute_command(companies_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.companies length: {len(companies)}")

            # mssp.api_token
            execute_command("SELECT * FROM mssp.api_tokens;")
            api_tokens = cursor.fetchall()

            if len(api_tokens) == 0:
                lock_api_tokens_command = "LOCK TABLES `api_tokens` WRITE;"
                api_tokens_command = "INSERT INTO `api_tokens` VALUES (1,'58637294-783a-443e-92ff-bb47222d93f8',1,'ISAC-Wizard','isac','','',0),(2,'0356a223-026e-45d0-b4db-660665c057cc',1,'LogMaster','lm','','',1),(3,'bd7dca5d-9108-458c-ab4e-1eb62212721d',1,'Alienvault','avt','','',1);"
                execute_command(lock_api_tokens_command)
                execute_command(api_tokens_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.api_tokens length: {len(api_tokens)}")

            # company_configs
            execute_command("SELECT * FROM mssp.company_configs;")
            company_configs = cursor.fetchall()

            if len(company_configs) == 0:
                lock_company_configs_command = "LOCK TABLES `company_configs` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                company_configs_command = f"INSERT INTO `company_configs` VALUES (1,1,'org_name','組織單位名稱','organization','system','{time}','Admin','{time}'),(2,1,'org_contact','組織單位聯絡人','organization','system','{time}','Admin','{time}'),(3,1,'org_tel','02-99999999','organization','system','{time}','Admin','{time}'),(4,1,'org_email','mail@mssp.com','organization','system','{time}','Admin','{time}'),(5,1,'org_submit_target','2','organization','system','{time}','Admin','{time}'),(6,1,'org_en_name','MSSP','organization','system','{time}','Admin','{time}'),(7,1,'soc_name','MSSP-SOC-NAME','organization','system','{time}','Admin','{time}'),(8,1,'org_no','org-no','organization','system','{time}','Admin','{time}'),(9,1,'otx_token','','license','system','{time}','Admin','{time}');"

                execute_command(lock_company_configs_command)
                execute_command(company_configs_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.company_configs length: {len(company_configs)}")

            # configs
            execute_command("SELECT * FROM mssp.configs;")
            configs = cursor.fetchall()

            if len(configs) == 0:
                lock_configs_command = "LOCK TABLES `configs` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                configs_command = f"INSERT INTO `configs` VALUES (1,'sys_hostname','mssp-portal','hostname','system','{time}','system','{time}'),(3,'sys_time_server','time.google.com','timeserver','system','{time}','system','{time}'),(4,'version','V2.0.0.1','system','system','{time}','system','{time}'),(5,'smtp_host','192.168.44.25','smtp','system','{time}','system','{time}'),(6,'smtp_port','25','smtp','system','{time}','system','{time}'),(7,'smtp_is_tls','0','smtp','system','{time}','system','{time}'),(8,'smtp_is_auth','0','smtp','system','{time}','system','{time}'),(9,'smtp_username','','smtp','system','{time}','system','{time}'),(10,'smtp_password','','smtp','system','{time}','system','{time}'),(11,'net_ip','192.168.69.194','network','system','{time}','system','{time}'),(12,'net_mask','255.255.255.0','network','system','{time}','system','{time}'),(13,'net_gateway','192.168.61.1','network','system','{time}','system','{time}'),(14,'net_dns','192.168.61.128','network','system','{time}','system','{time}'),(20,'smtp_sender','MSSP-Protal<support@billows.com.tw>','smtp','system','{time}','system','{time}'),(24,'notify_risk','3','notification_incident','system','{time}','system','{time}'),(25,'interval','1440','notification_incident','system','{time}','system','{time}'),(27,'receive_risk','1','notification_incident','system','{time}','system','{time}');"

                execute_command(lock_configs_command)
                execute_command(configs_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.configs length: {len(configs)}")

            # country
            execute_command("SELECT * FROM mssp.country;")
            country = cursor.fetchall()

            if len(country) == 0:
                lock_country_command = "LOCK TABLES `country` WRITE;"
                country_command = "INSERT INTO `country` VALUES (1,'AF','Afghanistan'),(2,'AX','Åland Islands'),(3,'AL','Albania'),(4,'DZ','Algeria'),(5,'AS','American Samoa'),(6,'AD','Andorra'),(7,'AO','Angola'),(8,'AI','Anguilla'),(9,'AQ','Antarctica'),(10,'AG','Antigua and Barbuda'),(11,'AR','Argentina'),(12,'AM','Armenia'),(13,'AW','Aruba'),(14,'AU','Australia'),(15,'AT','Austria'),(16,'AZ','Azerbaijan'),(17,'BS','Bahamas'),(18,'BH','Bahrain'),(19,'BD','Bangladesh'),(20,'BB','Barbados'),(21,'BY','Belarus'),(22,'BE','Belgium'),(23,'BZ','Belize'),(24,'BJ','Benin'),(25,'BM','Bermuda'),(26,'BT','Bhutan'),(27,'BO','Bolivia'),(28,'BQ','Bonaire'),(29,'BA','Bosnia and Herzegovina'),(30,'BW','Botswana'),(31,'BV','Bouvet Island'),(32,'BR','Brazil'),(33,'IO','British Indian Ocean Territory'),(34,'BN','Brunei Darussalam'),(35,'BG','Bulgaria'),(36,'BF','Burkina Faso'),(37,'BI','Burundi'),(38,'KH','Cambodia'),(39,'CM','Cameroon'),(40,'CA','Canada'),(41,'CV','Cape Verde'),(42,'KY','Cayman Islands'),(43,'CF','Central African Republic'),(44,'TD','Chad'),(45,'CL','Chile'),(46,'CN','China'),(47,'CX','Christmas Island'),(48,'CC','Cocos (Keeling) Islands'),(49,'CO','Colombia'),(50,'KM','Comoros'),(51,'CG','Congo'),(52,'CD','Congo the Democratic Republic of the'),(53,'CK','Cook Islands'),(54,'CR','Costa Rica'),(55,'CI','Ivory coast'),(56,'HR','Croatia'),(57,'CU','Cuba'),(58,'CW','Curaçao'),(59,'CY','Cyprus'),(60,'CZ','Czech Republic'),(61,'DK','Denmark'),(62,'DJ','Djibouti'),(63,'DM','Dominica'),(64,'DO','Dominican Republic'),(65,'EC','Ecuador'),(66,'EG','Egypt'),(67,'SV','El Salvador'),(68,'GQ','Equatorial Guinea'),(69,'ER','Eritrea'),(70,'EE','Estonia'),(71,'ET','Ethiopia'),(72,'FK','Falkland Islands (Malvinas)'),(73,'FO','Faroe Islands'),(74,'FJ','Fiji'),(75,'FI','Finland'),(76,'FR','France'),(77,'GF','French Guiana'),(78,'PF','French Polynesia'),(79,'TF','French Southern Territories'),(80,'GA','Gabon'),(81,'GM','Gambia'),(82,'GE','Georgia'),(83,'DE','Germany'),(84,'GH','Ghana'),(85,'GI','Gibraltar'),(86,'GR','Greece'),(87,'GL','Greenland'),(88,'GD','Grenada'),(89,'GP','Guadeloupe'),(90,'GU','Guam'),(91,'GT','Guatemala'),(92,'GG','Guernsey'),(93,'GN','Guinea'),(94,'GW','Guinea-Bissau'),(95,'GY','Guyana'),(96,'HT','Haiti'),(97,'HM','Heard Island and McDonald Islands'),(98,'VA','Holy See (Vatican City State)'),(99,'HN','Honduras'),(100,'HK','Hong Kong'),(101,'HU','Hungary'),(102,'IS','Iceland'),(103,'IN','India'),(104,'ID','Indonesia'),(105,'IR','Iran'),(106,'IQ','Iraq'),(107,'IE','Ireland'),(108,'IM','Isle of Man'),(109,'IL','Israel'),(110,'IT','Italy'),(111,'JM','Jamaica'),(112,'JP','Japan'),(113,'JE','Jersey'),(114,'JO','Jordan'),(115,'KZ','Kazakhstan'),(116,'KE','Kenya'),(117,'KI','Kiribati'),(118,'KP','North Korea'),(119,'KR','Korea'),(120,'KW','Kuwait'),(121,'KG','Kyrgyzstan'),(122,'LA','Lao People s Democratic Republic'),(123,'LV','Latvia'),(124,'LB','Lebanon'),(125,'LS','Lesotho'),(126,'LR','Liberia'),(127,'LY','Libya'),(128,'LI','Liechtenstein'),(129,'LT','Lithuania'),(130,'LU','Luxembourg'),(131,'MO','Macao'),(132,'MK','Macedonia'),(133,'MG','Madagascar'),(134,'MW','Malawi'),(135,'MY','Malaysia'),(136,'MV','Maldives'),(137,'ML','Mali'),(138,'MT','Malta'),(139,'MH','Marshall Islands'),(140,'MQ','Martinique'),(141,'MR','Mauritania'),(142,'MU','Mauritius'),(143,'YT','Mayotte'),(144,'MX','Mexico'),(145,'FM','Micronesia'),(146,'MD','Moldova'),(147,'MC','Monaco'),(148,'MN','Mongolia'),(149,'ME','Montenegro'),(150,'MS','Montserrat'),(151,'MA','Morocco'),(152,'MZ','Mozambique'),(153,'MM','Myanmar'),(154,'NA','Namibia'),(155,'NR','Nauru'),(156,'NP','Nepal'),(157,'NL','Netherlands'),(158,'NC','New Caledonia'),(159,'NZ','New Zealand'),(160,'NI','Nicaragua'),(161,'NE','Niger'),(162,'NG','Nigeria'),(163,'NU','Niue'),(164,'NF','Norfolk Island'),(165,'MP','Northern Mariana Islands'),(166,'NO','Norway'),(167,'OM','Oman'),(168,'PK','Pakistan'),(169,'PW','Palau'),(170,'PS','Palestine'),(171,'PA','Panama'),(172,'PG','Papua New Guinea'),(173,'PY','Paraguay'),(174,'PE','Peru'),(175,'PH','Philippines'),(176,'PN','Pitcairn'),(177,'PL','Poland'),(178,'PT','Portugal'),(179,'PR','Puerto Rico'),(180,'QA','Qatar'),(181,'RE','Réunion'),(182,'RO','Romania'),(183,'RU','Russian Federation'),(184,'RW','Rwanda'),(185,'BL','Saint Barthélemy'),(186,'SH','Saint Helena'),(187,'KN','Saint Kitts and Nevis'),(188,'LC','Saint Lucia'),(189,'MF','Saint Martin (French part)'),(190,'PM','Saint Pierre and Miquelon'),(191,'VC','Saint Vincent and the Grenadines'),(192,'WS','Samoa'),(193,'SM','San Marino'),(194,'ST','Sao Tome and Principe'),(195,'SA','Saudi Arabia'),(196,'SN','Senegal'),(197,'RS','Serbia'),(198,'SC','Seychelles'),(199,'SL','Sierra Leone'),(200,'SG','Singapore'),(201,'SX','Sint Maarten (Dutch part)'),(202,'SK','Slovakia'),(203,'SI','Slovenia'),(204,'SB','Solomon Islands'),(205,'SO','Somalia'),(206,'ZA','South Africa'),(207,'GS','South Georgia and the South Sandwich Islands'),(208,'SS','South Sudan'),(209,'ES','Spain'),(210,'LK','Sri Lanka'),(211,'SD','Sudan'),(212,'SR','Suriname'),(213,'SJ','Svalbard and Jan Mayen'),(214,'SZ','Swaziland'),(215,'SE','Sweden'),(216,'CH','Switzerland'),(217,'SY','Syrian Arab Republic'),(218,'TW','Taiwan'),(219,'TJ','Tajikistan'),(220,'TZ','Tanzania United Republic of'),(221,'TH','Thailand'),(222,'TL','Timor-Leste'),(223,'TG','Togo'),(224,'TK','Tokelau'),(225,'TO','Tonga'),(226,'TT','Trinidad and Tobago'),(227,'TN','Tunisia'),(228,'TR','Turkey'),(229,'TM','Turkmenistan'),(230,'TC','Turks and Caicos Islands'),(231,'TV','Tuvalu'),(232,'UG','Uganda'),(233,'UA','Ukraine'),(234,'AE','United Arab Emirates'),(235,'GB','United Kingdom'),(236,'US','United States'),(237,'UM','United States Minor Outlying Islands'),(238,'UY','Uruguay'),(239,'UZ','Uzbekistan'),(240,'VU','Vanuatu'),(241,'VE','Venezuela'),(242,'VN','Viet Nam'),(243,'VG','Virgin Islands British'),(244,'VI','Virgin Islands U.S.'),(245,'WF','Wallis and Futuna'),(246,'EH','Western Sahara'),(247,'YE','Yemen'),(248,'ZM','Zambia'),(249,'ZW','Zimbabwe');"

                execute_command(lock_country_command)
                execute_command(country_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.country length: {len(country)}")

            # dashboard_widgets
            execute_command("SELECT * FROM mssp.dashboard_widgets;")
            dashboard_widgets = cursor.fetchall()

            if len(dashboard_widgets) == 0:
                lock_dashboard_widgets_command = "LOCK TABLES `dashboard_widgets` WRITE;"
                dashboard_widgets_command = "INSERT INTO `dashboard_widgets` VALUES (1,'15030164-e1ec-4414-a72b-e90993a986a5','INCIDENT_RISK','/mssp/api/1.0/info-center/dashboard/stats/incident-risk','mssp',1),(2,'b6853059-ad7b-418d-a704-c700ca102002','ACCIDENT_VERIFY_STATUS','/mssp/api/1.0/info-center/dashboard/stats/accident-verify-status','mssp',1),(3,'b27f75f2-6e02-4e7b-af51-509bdf04bc60','IOC','/mssp/api/1.0/info-center/dashboard/stats/ioc','mssp',1),(4,'2509fde8-8b6e-4baa-92f5-024ac3e73535','IOC_COUNT','/mssp/api/1.0/info-center/dashboard/stats/ioc-count','mssp',1),(5,'3416998b-da74-4c6a-a9ba-827cf1f3c58b','PULSES','/mssp/api/1.0/info-center/dashboard/stats/pulses','mssp',1),(6,'65861535-31ad-4923-adba-2a52aec3eb8c','MALWARE','/mssp/api/1.0/info-center/dashboard/stats/malware','mssp',1),(7,'2b962c2d-9eff-43e0-bb79-4c195d3f2a16','THREAT','/mssp/api/1.0/info-center/dashboard/stats/threat','mssp',0),(8,'ca2fe469-eeb0-4127-9055-03e0a2385802','LOG_EPS','/mssp/api/1.0/info-center/dashboard/stats/log-eps','lm',1),(9,'7ea89544-0d82-43cf-a2a6-0693b98749c2','ATTACK_COUNTRY','/mssp/api/1.0/info-center/dashboard/stats/attack-country','mssp',1),(10,'60043d1a-a3dd-434b-afeb-d5dd4ee748ea','ATTACK_INTENT','/mssp/api/1.0/info-center/dashboard/stats/attack-intent','mssp',1),(11,'00648873-b5bd-4972-b067-09abdc52e12f','DEVICE_REGION_TOPOLOGY','/mssp/api/1.0/info-center/dashboard/device/region','mssp',1),(12,'ad5d12a6-f249-4b4b-8386-8a4b9b1a687d','WINDOWS_EVENT','/mssp/api/1.0/dashboard/stats/windows_event','lm','1'),(13,'bfce38d8-4def-4ec6-aded-ec9d545f73d0','LINUX_EVENT','/mssp/api/1.0/dashboard/stats/linux_event','lm','1'),(14,'8ec92577-6e13-45bb-b2b7-2af01d5060a6','STATISTICS_IP','/mssp/api/1.0/dashboard/stats/statistics_ip','lm','1');"

                execute_command(lock_dashboard_widgets_command)
                execute_command(dashboard_widgets_command)
                execute_command(close_command)

            # device_groups
            execute_command("SELECT * FROM mssp.device_groups;")
            device_groups = cursor.fetchall()

            if len(device_groups) == 0:
                lock_device_group_command = "LOCK TABLES `device_groups` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                device_group_command = f"INSERT INTO `device_groups` VALUES (1,1,'30bdd22a-f8c1-48f5-a42b-537342d3d346','Default Group','IT',1,1,0,'','預設群組','system','{time}','test001','{time}');"

                execute_command(lock_device_group_command)
                execute_command(device_group_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.device_groups length: {len(device_groups)}")

            # global_menu
            execute_command("SELECT * FROM mssp.global_menu;")
            global_menu = cursor.fetchall()

            if len(global_menu) == 0:
                lock_global_menu_command = "LOCK TABLES `global_menu` WRITE;"
                global_menu_command = "INSERT INTO `global_menu` VALUES (1,0,'OT001','OT機台','device_type',1),(2,0,'OT002','機械手臂','device_type',1),(3,0,'OT003','伺服試沖床','device_type',1),(4,0,'OT004','沖壓機','device_type',1),(5,0,'OT005','AOI光學檢測','device_type',1),(6,0,'OT006','雷射雕刻站','device_type',1),(7,0,'OT007','出料線','device_type',1),(8,0,'IT001','Server','device_type',1),(9,0,'IT002','Linux','device_type',1),(10,0,'IT003','Windows','device_type',1),(11,0,'IT004','筆記型電腦','device_type',1),(12,0,'IT005','桌上型電腦','device_type',1),(13,0,'IT006','Firewall','device_type',1),(14,0,'IT007','Switch','device_type',1),(15,0,'IT008','印表機','device_type',1),(16,0,'IT009','WIFI-AP','device_type',1),(17,0,'IT010','Storage','device_type',1),(18,0,'IT011','IOS','device_type',1),(19,0,'IT012','Android','device_type',1),(20,0,'IT013','NAS','device_type',1),(21,0,'IT','IT設備群組','device_group_type',1),(22,0,'OT','OT設備群組','device_group_type',1),(23,0,'CUST_1','客製化-1群組','device_group_type',1),(24,0,'avt','AlienVault','sensor_type',1),(25,0,'lm','LogMasterV4','sensor_type',1),(26,0,'tachometer','fas fa-tachometer-alt','icon',1),(27,0,'shield','fas fa-shield-alt','icon',1),(28,0,'shield-virus','fas fa-shield-virus','icon',1),(29,0,'cogs','fas fa-cogs','icon',1),(30,0,'align-left','fas fa-align-left','icon',1),(31,0,'desktop','fas fa-desktop','icon',1),(32,0,'table','fas fa-table','icon',1),(33,0,'crossbones','fas fa-skull-crossbones','icon',1),(34,0,'scroll','fas fa-scroll','icon',1),(35,0,'dragon','fas fa-dragon','icon',1),(36,0,'chart-bar','fas fa-chart-bar','icon',1),(37,0,'chart-line','fas fa-chart-line','icon',1),(38,0,'chart-pie','fas fa-chart-pie','icon',1),(39,0,'globe','fas fa-globe','icon',1),(40,0,'spider','fas fa-spider','icon',1),(41,0,'grunt','fab fa-grunt','icon',1),(42,0,'accessible','fab fa-accessible-icon','icon',1),(43,0,'virus','fas fa-virus','icon',1),(44,0,'exclamation-triangle','fas fa-exclamation-triangle','icon',1),(45,0,'radiation','fas fa-radiation','icon',1),(46,0,'server','fas fa-server','icon',1),(47,0,'hdd','fas fa-hdd','icon',1),(48,0,'power-off','fas fa-power-off','icon',1),(49,0,'database','fas fa-database','icon',1),(50,0,'ethernet','fas fa-ethernet','icon',1);"

                execute_command(lock_global_menu_command)
                execute_command(global_menu_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.global_menu length: {len(global_menu)}")

            # operations
            execute_command("SELECT * FROM mssp.operations;")
            operations = cursor.fetchall()

            if len(operations) == 0:
                lock_operations_command = "LOCK TABLES `operations` WRITE;"
                operations_command = "INSERT INTO `operations` VALUES (1,'CREATE'),(2,'UPDATE'),(3,'DELETE'),(4,'VIEW'),(5,'VERIFY'),(6,'EXPORT'),(7,'SUBMIT'),(8,'DOWNLOAD'),(9,'REJECT'),(10,'ARCHIVE'),(11,'UPLOAD');"

                execute_command(lock_operations_command)
                execute_command(operations_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.operations length: {len(operations)}")

            # permissions
            execute_command("SELECT * FROM mssp.permissions;")
            permissions = cursor.fetchall()

            if len(permissions) == 0:
                lock_permissions_command = "LOCK TABLES `permissions` WRITE;"
                permissions_command = "INSERT INTO `permissions` VALUES (1,'USER_MANAGE',1,'/user/user-manage'),(2,'ROLE_MANAGE',1,'/user/role-manage'),(3,'DEVICE_MANAGE',1,'/device/device-manage'),(4,'DEVICE_GROUP_MANAGE',1,'/device/device-group-manage'),(5,'SYSTEM_CONFIGURE',1,'/configure/system'),(6,'DASHBOARD_TEMPLATE_MANAGE',1,'/dashboard-template/dashboard-template-manage'),(7,'DASHBOARD',1,'/dashboard'),(8,'DATA_MIGRATE_MANAGE',1,'/data-migrate/data-migrate-manage'),(9,'COMPANY_MANAGE',1,'/company/company-manage'),(10,'SENSOR_MANAGE',1,'/sensor/sensor-manage'),(11,'INCIDENT_MANAGE',1,'/security/incident-manage'),(12,'ACCIDENT_MANAGE',1,'/security/accident-manage'),(13,'ACCIDENT_VERIFY_MANAGE',1,'/security/accident-verify-manage'),(14,'ACCIDENT_VERIFY_FLOW_MANAGE',1,'/configure/subordinate'),(15,'STATISTICS_REPORT',1,'/report/statistics-report'),(16,'SCHEDULE_REPORT_MANAGE',1,'/report/schedule-report'),(17,'SMTP_CONFIGURE',1,'/configure/smtp'),(18,'ACCIDENT_SUBMIT_CONFIGURE',1,'/configure/accident-submit'),(19, 'SENTIMENT_MANAGE', 1, '/pulse/sentiment-manage'), (20, 'PULSE_MANAGE', 1, '/pulse/create-manage'), (21, 'OPERATION_RECORD_MANAGE', 1, '/record/operation-manage'), (22, 'AUDIT_MANAGE', 1, '/clause/clause-manager'),(23, 'CLAUSE_TYPE_MANAGE', 1, '/clause/type-manager');"

                execute_command(lock_permissions_command)
                execute_command(permissions_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.permissions length: {len(permissions)}")

            # reports
            execute_command("SELECT * FROM mssp.reports;")
            reports = cursor.fetchall()

            if len(reports) == 0:
                lock_reports_command = "LOCK TABLES `reports` WRITE;"
                reports_command = "INSERT INTO `reports` VALUES (1,'89b40409-5446-4f29-8fb8-aa78a05edeb1','UNTREATED_INCIDENT_REPORT',1,1),(2,'6682e33e-add8-4ea3-a9b8-e5a22b4b0710','UNTREATED_ACCIDENT_REPORT',1,1),(3,'8f25f3b7-0d50-4f66-b9d3-611481bb7861','SUBMITTED_ACCIDENT_REPORT',1,1);"

                execute_command(lock_reports_command)
                execute_command(reports_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.reports length: {len(reports)}")

            # roles
            execute_command("SELECT * FROM mssp.roles;")
            roles = cursor.fetchall()

            if len(roles) == 0:
                lock_roles_command = "LOCK TABLES `roles` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                roles_command = f"INSERT INTO `roles` VALUES (1,'164a3a05-867e-4a52-a6eb-7142ff44fe2e',1,'Administrator','Administrator Role','{time}','{time}');"

                execute_command(lock_roles_command)
                execute_command(roles_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.roles length: {len(roles)}")

            # roles_permissions
            execute_command("SELECT * FROM mssp.roles_permissions;")
            roles_permissions = cursor.fetchall()

            if len(roles_permissions) == 0:
                lock_roles_permissions_command = "LOCK TABLES `roles_permissions` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # roles_permissions_command = "INSERT INTO `roles_permissions` VALUES (1,1,1,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(2,1,1,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(3,1,1,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(4,1,1,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(5,1,2,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(6,1,2,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(7,1,2,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(8,1,2,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(9,1,3,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(10,1,3,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(11,1,3,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(12,1,3,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(13,1,4,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(14,1,4,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(15,1,4,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(16,1,4,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(17,1,5,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(18,1,5,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(19,1,6,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(20,1,6,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(21,1,6,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(22,1,6,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(23,1,7,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(24,1,8,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(25,1,8,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(26,1,9,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(27,1,9,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(28,1,9,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(29,1,9,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(30,1,10,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(31,1,10,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(32,1,10,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(33,1,10,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(34,1,11,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(35,1,11,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(36,1,11,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(37,1,11,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(38,1,11,7,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(39,1,11,8,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(40,1,11,10,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(41,1,12,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(42,1,12,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(43,1,12,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(44,1,12,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(45,1,12,7,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(46,1,12,8,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(47,1,12,10,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(48,1,13,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(49,1,13,5,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(50,1,13,9,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(51,1,14,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(52,1,14,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(53,1,14,3,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(54,1,14,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(55,1,15,4,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(56,1,15,6,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(57,1,16,1,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(58,1,16,2,0,'2021-09-27 14:53:54','2021-09-27 14:53:54'),(59,1,16,3,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(60,1,16,4,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(61,1,16,8,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(62,1,17,2,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(63,1,17,4,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(64,1,18,2,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'),(65,1,18,4,0,'2021-09-27 14:53:55','2021-09-27 14:53:55'), (66, 1, 19, 4, 0, '2021-09-27 14:53:55', '2021-09-27 14:53:55'), (67, 1, 20, 1, 0, '2021-09-27 14:53:55', '2021-09-27 14:53:55'), (68, 1, 20, 3, 0, '2021-09-27 14:53:55', '2021-09-27 14:53:55'), (69, 1, 20, 4, 0, '2021-09-27 14:53:55', '2021-09-27 14:53:55');"
                roles_permissions_command = f"INSERT INTO `roles_permissions` (`roles_id`,`permissions_id`,`operations_id`,`is_revoked`,`create_at`,`update_at`) VALUES (1,1,1,0,'{time}','{time}'),(1,1,2,0,'{time}','{time}'),(1,1,3,0,'{time}','{time}'),(1,1,4,0,'{time}','{time}'),(1,2,1,0,'{time}','{time}'),(1,2,2,0,'{time}','{time}'),(1,2,3,0,'{time}','{time}'),(1,2,4,0,'{time}','{time}'),(1,3,1,0,'{time}','{time}'),(1,3,2,0,'{time}','{time}'),(1,3,3,0,'{time}','{time}'),(1,3,4,0,'{time}','{time}'),(1,4,1,0,'{time}','{time}'),(1,4,2,0,'{time}','{time}'),(1,4,3,0,'{time}','{time}'),(1,4,4,0,'{time}','{time}'),(1,5,2,0,'{time}','{time}'),(1,5,4,0,'{time}','{time}'),(1,6,1,0,'{time}','{time}'),(1,6,2,0,'{time}','{time}'),(1,6,3,0,'{time}','{time}'),(1,6,4,0,'{time}','{time}'),(1,7,4,0,'{time}','{time}'),(1,8,2,0,'{time}','{time}'),(1,8,4,0,'{time}','{time}'),(1,9,1,0,'{time}','{time}'),(1,9,2,0,'{time}','{time}'),(1,9,3,0,'{time}','{time}'),(1,9,4,0,'{time}','{time}'),(1,10,1,0,'{time}','{time}'),(1,10,2,0,'{time}','{time}'),(1,10,3,0,'{time}','{time}'),(1,10,4,0,'{time}','{time}'),(1,11,1,0,'{time}','{time}'),(1,11,2,0,'{time}','{time}'),(1,11,3,0,'{time}','{time}'),(1,11,4,0,'{time}','{time}'),(1,11,7,0,'{time}','{time}'),(1,11,8,0,'{time}','{time}'),(1,11,10,0,'{time}','{time}'),(1,12,1,0,'{time}','{time}'),(1,12,2,0,'{time}','{time}'),(1,12,3,0,'{time}','{time}'),(1,12,4,0,'{time}','{time}'),(1,12,7,0,'{time}','{time}'),(1,12,8,0,'{time}','{time}'),(1,12,10,0,'{time}','{time}'),(1,13,4,0,'{time}','{time}'),(1,13,5,0,'{time}','{time}'),(1,13,9,0,'{time}','{time}'),(1,14,1,0,'{time}','{time}'),(1,14,2,0,'{time}','{time}'),(1,14,3,0,'{time}','{time}'),(1,14,4,0,'{time}','{time}'),(1,15,4,0,'{time}','{time}'),(1,15,6,0,'{time}','{time}'),(1,16,1,0,'{time}','{time}'),(1,16,2,0,'{time}','{time}'),(1,16,3,0,'{time}','{time}'),(1,16,4,0,'{time}','{time}'),(1,16,8,0,'{time}','{time}'),(1,17,2,0,'{time}','{time}'),(1,17,4,0,'{time}','{time}'),(1,18,2,0,'{time}','{time}'),(1,18,4,0,'{time}','{time}'),(1,19,4,0,'{time}','{time}'),(1,20,1,0,'{time}','{time}'),(1,20,2,0,'{time}','{time}'),(1,20,3,0,'{time}','{time}'),(1,20,4,0,'{time}','{time}'),(1,21,4,0,'{time}','{time}'),(1,21,8,0,'{time}','{time}'),(1,22,1,0,'{time}','{time}'),(1,22,2,0,'{time}','{time}'),(1,22,3,0,'{time}','{time}'),(1,22,4,0,'{time}','{time}'),(1,22,8,0,'{time}','{time}'),(1,22,11,0,'{time}','{time}'),(1,23,1,0,'{time}','{time}'),(1,23,2,0,'{time}','{time}'),(1,23,3,0,'{time}','{time}'),(1,23,4,0,'{time}','{time}');"

                execute_command(lock_roles_permissions_command)
                execute_command(roles_permissions_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.roles_permissions length: {len(roles_permissions)}")

            # submit_organizations
            execute_command("SELECT * FROM mssp.submit_organizations;")
            submit_organizations = cursor.fetchall()

            if len(submit_organizations) == 0:
                lock_submit_organizations_command = "LOCK TABLES `submit_organizations` WRITE;"
                submit_organizations_command = "INSERT INTO `submit_organizations` VALUES (1,'nccst','技服中心','SFTP',NULL,NULL,NULL),(2,'twcert','台灣電腦網路危機處理暨協調中心','EMAIL',NULL,NULL,NULL);"

                execute_command(lock_submit_organizations_command)
                execute_command(submit_organizations_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.submit_organizations length: {len(submit_organizations)}")

            # users
            execute_command("SELECT * FROM mssp.users;")
            users = cursor.fetchall()

            if len(users) == 0:
                lock_users_command = "LOCK TABLES `users` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                users_command = f"INSERT INTO `users` VALUES (1,'2076fa80-e2ab-37e0-b9dc-1ff122fffa2b',1,'Admin','Administrator','0987654321','$2b$12$Pf7l/hMmzxqpjlfMolR.1.3ztGRsK.mhPO6tjDAYOwkaeXPr.MJzu','admin@mssp.com',1,0,0,1,'{time}','{time}');"

                execute_command(lock_users_command)
                execute_command(users_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.users length: {len(users)}")

            # user_dashboard
            execute_command("SELECT * FROM mssp.user_dashboard;")
            user_dashboards = cursor.fetchall()

            if len(user_dashboards) == 0:
                lock_user_dashboards_command = "LOCK TABLES `user_dashboard` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_dashboard_command = f"INSERT INTO `user_dashboard` VALUES ('1','d31fe301-9998-445d-a55c-82779d52966a','1','儀表板','fas fa-tachometer-alt','預設儀表板','Admin','{time}','Admin','{time}');"

                execute_command(lock_user_dashboards_command)
                execute_command(user_dashboard_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.user_dashboard length: {len(user_dashboards)}")

            # user_dashboard_widgets
            execute_command("SELECT * FROM mssp.user_dashboard_widgets;")
            user_dashboard_widgets = cursor.fetchall()

            if len(user_dashboard_widgets) == 0:
                lock_user_dashboard_widgets_command = "LOCK TABLES `user_dashboard_widgets` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_dashboard_widget_command = f"INSERT INTO `user_dashboard_widgets` VALUES ('1','bf768458-f62d-4241-8b0c-560a0742341e','1','1','6','4','0','0','0','Admin','{time}','Admin','{time}'),('2','0c00343b-7426-4515-af7f-4eaec6ccea5a','1','2','6','4','6','0','1','Admin','{time}','Admin','{time}'),('3','1fbe7e37-f13c-4351-bded-585cb23b406d','1','4','6','13','0','15','2','Admin','{time}','Admin','{time}'),('4','c74feafd-a181-4d36-b841-d64203f1b3da','1','11','6','13','6','15','3','Admin','{time}','Admin','{time}'),('5','e2277f6f-b73f-49c2-8e6c-a210b0046134','1','10','12','11','0','4','4','Admin','{time}','Admin','{time}'),('6','306adec8-b8c5-4217-8ff3-4b670874fa1a','1','3','3','12','0','28','5','Admin','{time}','Admin','{time}'),('7','0617b7d9-158d-4f56-a458-5e7bc732821f','1','5','3','12','3','28','6','Admin','{time}','Admin','{time}'),('8','978073c2-f6ba-4522-a204-51e2bf295b36','1','6','6','12','6','28','7','Admin','{time}','Admin','{time}');"

                execute_command(lock_user_dashboard_widgets_command)
                execute_command(user_dashboard_widget_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.user_dashboard_widgets length: {len(user_dashboard_widgets)}")

            # zip
            execute_command("SELECT * FROM mssp.zip;")
            zip = cursor.fetchall()

            if len(zip) == 0:
                lock_zip_command = "LOCK TABLES `zip` WRITE;"
                zip_command = "INSERT INTO `zip` VALUES (1,'TPE','100','中正區'),(2,'TPE','103','大同區'),(3,'TPE','104','中山區'),(4,'TPE','105','松山區'),(5,'TPE','106','大安區'),(6,'TPE','108','萬華區'),(7,'TPE','110','信義區'),(8,'TPE','111','士林區'),(9,'TPE','112','北投區'),(10,'TPE','114','內湖區'),(11,'TPE','115','南港區'),(12,'TPE','116','文山區'),(13,'KEE','200','仁愛區'),(14,'KEE','201','信義區'),(15,'KEE','202','中正區'),(16,'KEE','203','中山區'),(17,'KEE','204','安樂區'),(18,'KEE','205','暖暖區'),(19,'KEE','206','七堵區'),(20,'TPQ','207','萬里區'),(21,'TPQ','208','金山區'),(22,'TPQ','220','板橋區'),(23,'TPQ','221','汐止區'),(24,'TPQ','222','深坑區'),(25,'TPQ','223','石碇區'),(26,'TPQ','224','瑞芳區'),(27,'TPQ','226','平溪區'),(28,'TPQ','227','雙溪區'),(29,'TPQ','228','貢寮區'),(30,'TPQ','231','新店區'),(31,'TPQ','232','坪林區'),(32,'TPQ','233','烏來區'),(33,'TPQ','234','永和區'),(34,'TPQ','235','中和區'),(35,'TPQ','236','土城區'),(36,'TPQ','237','三峽區'),(37,'TPQ','238','樹林區'),(38,'TPQ','239','鶯歌區'),(39,'TPQ','241','三重區'),(40,'TPQ','242','新莊區'),(41,'TPQ','243','泰山區'),(42,'TPQ','244','林口區'),(43,'TPQ','247','蘆洲區'),(44,'TPQ','248','五股區'),(45,'TPQ','249','八里區'),(46,'TPQ','251','淡水區'),(47,'TPQ','252','三芝區'),(48,'TPQ','253','石門區'),(49,'ILA','260','宜蘭市'),(50,'ILA','261','頭城鎮'),(51,'ILA','262','礁溪鄉'),(52,'ILA','263','壯圍鄉'),(53,'ILA','264','員山鄉'),(54,'ILA','265','羅東鎮'),(55,'ILA','266','三星鄉'),(56,'ILA','267','大同鄉'),(57,'ILA','268','五結鄉'),(58,'ILA','269','冬山鄉'),(59,'ILA','270','蘇澳鎮'),(60,'ILA','272','南澳鄉'),(61,'ILA','290','釣魚臺列嶼'),(63,'HSZ','300_1','東區'),(64,'HSZ','300_2','北區'),(65,'HSZ','300_3','香山區'),(66,'HSQ','302','竹北市'),(67,'HSQ','303','湖口鄉'),(68,'HSQ','304','新豐鄉'),(69,'HSQ','305','新埔鎮'),(70,'HSQ','306','關西鎮'),(71,'HSQ','307','芎林鄉'),(72,'HSQ','308','寶山鄉'),(73,'HSQ','310','竹東鎮'),(74,'HSQ','311','五峰鄉'),(75,'HSQ','312','橫山鄉'),(76,'HSQ','313','尖石鄉'),(77,'HSQ','314','北埔鄉'),(78,'HSQ','315','峨眉鄉'),(79,'TAO','320','中壢區'),(80,'TAO','324','平鎮區'),(81,'TAO','325','龍潭區'),(82,'TAO','326','楊梅區'),(83,'TAO','327','新屋區'),(84,'TAO','328','觀音區'),(85,'TAO','330','桃園區'),(86,'TAO','333','龜山區'),(87,'TAO','334','八德區'),(88,'TAO','335','大溪區'),(89,'TAO','336','復興區'),(90,'TAO','337','大園區'),(91,'TAO','338','蘆竹區'),(92,'MIA','350','竹南鎮'),(93,'MIA','351','頭份市'),(94,'MIA','352','三灣鄉'),(95,'MIA','353','南庄鄉'),(96,'MIA','354','獅潭鄉'),(97,'MIA','356','後龍鎮'),(98,'MIA','357','通霄鎮'),(99,'MIA','358','苑裡鎮'),(100,'MIA','360','苗栗市'),(101,'MIA','361','造橋鄉'),(102,'MIA','362','頭屋鄉'),(103,'MIA','363','公館鄉'),(104,'MIA','364','大湖鄉'),(105,'MIA','365','泰安鄉'),(106,'MIA','366','銅鑼鄉'),(107,'MIA','367','三義鄉'),(108,'MIA','368','西湖鄉'),(109,'MIA','369','卓蘭鎮'),(110,'TXG','400','中區'),(111,'TXG','401','東區'),(112,'TXG','402','南區'),(113,'TXG','403','西區'),(114,'TXG','404','北區'),(115,'TXG','406','北屯區'),(116,'TXG','407','西屯區'),(117,'TXG','408','南屯區'),(118,'TXG','411','太平區'),(119,'TXG','412','大里區'),(120,'TXG','413','霧峰區'),(121,'TXG','414','烏日區'),(122,'TXG','420','豐原區'),(123,'TXG','421','后里區'),(124,'TXG','422','石岡區'),(125,'TXG','423','東勢區'),(126,'TXG','424','和平區'),(127,'TXG','426','新社區'),(128,'TXG','427','潭子區'),(129,'TXG','428','大雅區'),(130,'TXG','429','神岡區'),(131,'TXG','432','大肚區'),(132,'TXG','433','沙鹿區'),(133,'TXG','434','龍井區'),(134,'TXG','435','梧棲區'),(135,'TXG','436','清水區'),(136,'TXG','437','大甲區'),(137,'TXG','438','外埔區'),(138,'TXG','439','大安區'),(139,'CHA','500','彰化市'),(140,'CHA','502','芬園鄉'),(141,'CHA','503','花壇鄉'),(142,'CHA','504','秀水鄉'),(143,'CHA','505','鹿港鎮'),(144,'CHA','506','福興鄉'),(145,'CHA','507','線西鄉'),(146,'CHA','508','和美鎮'),(147,'CHA','509','伸港鄉'),(148,'CHA','510','員林市'),(149,'CHA','511','社頭鄉'),(150,'CHA','512','永靖鄉'),(151,'CHA','513','埔心鄉'),(152,'CHA','514','溪湖鎮'),(153,'CHA','515','大村鄉'),(154,'CHA','516','埔鹽鄉'),(155,'CHA','520','田中鎮'),(156,'CHA','521','北斗鎮'),(157,'CHA','522','田尾鄉'),(158,'CHA','523','埤頭鄉'),(159,'CHA','524','溪州鄉'),(160,'CHA','525','竹塘鄉'),(161,'CHA','526','二林鎮'),(162,'CHA','527','大城鄉'),(163,'CHA','528','芳苑鄉'),(164,'CHA','530','二水鄉'),(165,'NAN','540','南投市'),(166,'NAN','541','中寮鄉'),(167,'NAN','542','草屯鎮'),(168,'NAN','544','國姓鄉'),(169,'NAN','545','埔里鎮'),(170,'NAN','546','仁愛鄉'),(171,'NAN','551','名間鄉'),(172,'NAN','552','集集鎮'),(173,'NAN','553','水里鄉'),(174,'NAN','555','魚池鄉'),(175,'NAN','556','信義鄉'),(176,'NAN','557','竹山鎮'),(177,'NAN','558','鹿谷鄉'),(179,'CYI','600_1','東區'),(180,'CYI','600_2','西區'),(181,'CYQ','602','番路鄉'),(182,'CYQ','603','梅山鄉'),(183,'CYQ','604','竹崎鄉'),(184,'CYQ','605','阿里山鄉'),(185,'CYQ','606','中埔鄉'),(186,'CYQ','607','大埔鄉'),(187,'CYQ','608','水上鄉'),(188,'CYQ','611','鹿草鄉'),(189,'CYQ','612','太保市'),(190,'CYQ','613','朴子市'),(191,'CYQ','614','東石鄉'),(192,'CYQ','615','六腳鄉'),(193,'CYQ','616','新港鄉'),(194,'CYQ','621','民雄鄉'),(195,'CYQ','622','大林鎮'),(196,'CYQ','623','溪口鄉'),(197,'CYQ','624','義竹鄉'),(198,'CYQ','625','布袋鎮'),(199,'YUN','630','斗南鎮'),(200,'YUN','631','大埤鄉'),(201,'YUN','632','虎尾鎮'),(202,'YUN','633','土庫鎮'),(203,'YUN','634','褒忠鄉'),(204,'YUN','635','東勢鄉'),(205,'YUN','636','臺西鄉'),(206,'YUN','637','崙背鄉'),(207,'YUN','638','麥寮鄉'),(208,'YUN','640','斗六市'),(209,'YUN','643','林內鄉'),(210,'YUN','646','古坑鄉'),(211,'YUN','647','莿桐鄉'),(212,'YUN','648','西螺鎮'),(213,'YUN','649','二崙鄉'),(214,'YUN','651','北港鎮'),(215,'YUN','652','水林鄉'),(216,'YUN','653','口湖鄉'),(217,'YUN','654','四湖鄉'),(218,'YUN','655','元長鄉'),(219,'TNN','700','中西區'),(220,'TNN','701','東區'),(221,'TNN','702','南區'),(222,'TNN','704','北區'),(223,'TNN','708','安平區'),(224,'TNN','709','安南區'),(225,'TNN','710','永康區'),(226,'TNN','711','歸仁區'),(227,'TNN','712','新化區'),(228,'TNN','713','左鎮區'),(229,'TNN','714','玉井區'),(230,'TNN','715','楠西區'),(231,'TNN','716','南化區'),(232,'TNN','717','仁德區'),(233,'TNN','718','關廟區'),(234,'TNN','719','龍崎區'),(235,'TNN','720','官田區'),(236,'TNN','721','麻豆區'),(237,'TNN','722','佳里區'),(238,'TNN','723','西港區'),(239,'TNN','724','七股區'),(240,'TNN','725','將軍區'),(241,'TNN','726','學甲區'),(242,'TNN','727','北門區'),(243,'TNN','730','新營區'),(244,'TNN','731','後壁區'),(245,'TNN','732','白河區'),(246,'TNN','733','東山區'),(247,'TNN','734','六甲區'),(248,'TNN','735','下營區'),(249,'TNN','736','柳營區'),(250,'TNN','737','鹽水區'),(251,'TNN','741','善化區'),(252,'TNN','742','大內區'),(253,'TNN','743','山上區'),(254,'TNN','744','新市區'),(255,'TNN','745','安定區'),(256,'KHH','800','新興區'),(257,'KHH','801','前金區'),(258,'KHH','802','苓雅區'),(259,'KHH','803','鹽埕區'),(260,'KHH','804','鼓山區'),(261,'KHH','805','旗津區'),(262,'KHH','806','前鎮區'),(263,'KHH','807','三民區'),(264,'KHH','811','楠梓區'),(265,'KHH','812','小港區'),(266,'KHH','813','左營區'),(267,'KHH','814','仁武區'),(268,'KHH','815','大社區'),(269,'KHH','820','岡山區'),(270,'KHH','821','路竹區'),(271,'KHH','822','阿蓮區'),(272,'KHH','823','田寮區'),(273,'KHH','824','燕巢區'),(274,'KHH','825','橋頭區'),(275,'KHH','826','梓官區'),(276,'KHH','827','彌陀區'),(277,'KHH','828','永安區'),(278,'KHH','829','湖內區'),(279,'KHH','830','鳳山區'),(280,'KHH','831','大寮區'),(281,'KHH','832','林園區'),(282,'KHH','833','鳥松區'),(283,'KHH','840','大樹區'),(284,'KHH','842','旗山區'),(285,'KHH','843','美濃區'),(286,'KHH','844','六龜區'),(287,'KHH','845','內門區'),(288,'KHH','846','杉林區'),(289,'KHH','847','甲仙區'),(290,'KHH','848','桃源區'),(291,'KHH','849','那瑪夏區'),(292,'KHH','851','茂林區'),(293,'KHH','852','茄萣區'),(294,'LJF','817','東沙'),(295,'LJF','819','南沙'),(296,'PEN','880','馬公市'),(297,'PEN','881','西嶼鄉'),(298,'PEN','882','望安鄉'),(299,'PEN','883','七美鄉'),(300,'PEN','884','白沙鄉'),(301,'PEN','885','湖西鄉'),(302,'PIF','900','屏東市'),(303,'PIF','901','三地門鄉'),(304,'PIF','902','霧臺鄉'),(305,'PIF','903','瑪家鄉'),(306,'PIF','904','九如鄉'),(307,'PIF','905','里港鄉'),(308,'PIF','906','高樹鄉'),(309,'PIF','907','鹽埔鄉'),(310,'PIF','908','長治鄉'),(311,'PIF','909','麟洛鄉'),(312,'PIF','911','竹田鄉'),(313,'PIF','912','內埔鄉'),(314,'PIF','913','萬丹鄉'),(315,'PIF','920','潮州鎮'),(316,'PIF','921','泰武鄉'),(317,'PIF','922','來義鄉'),(318,'PIF','923','萬巒鄉'),(319,'PIF','924','崁頂鄉'),(320,'PIF','925','新埤鄉'),(321,'PIF','926','南州鄉'),(322,'PIF','927','林邊鄉'),(323,'PIF','928','東港鎮'),(324,'PIF','929','琉球鄉'),(325,'PIF','931','佳冬鄉'),(326,'PIF','932','新園鄉'),(327,'PIF','940','枋寮鄉'),(328,'PIF','941','枋山鄉'),(329,'PIF','942','春日鄉'),(330,'PIF','943','獅子鄉'),(331,'PIF','944','車城鄉'),(332,'PIF','945','牡丹鄉'),(333,'PIF','946','恆春鎮'),(334,'PIF','947','滿州鄉'),(335,'TTT','950','臺東市'),(336,'TTT','951','綠島鄉'),(337,'TTT','952','蘭嶼鄉'),(338,'TTT','953','延平鄉'),(339,'TTT','954','卑南鄉'),(340,'TTT','955','鹿野鄉'),(341,'TTT','956','關山鎮'),(342,'TTT','957','海端鄉'),(343,'TTT','958','池上鄉'),(344,'TTT','959','東河鄉'),(345,'TTT','961','成功鎮'),(346,'TTT','962','長濱鄉'),(347,'TTT','963','太麻里鄉'),(348,'TTT','964','金峰鄉'),(349,'TTT','965','大武鄉'),(350,'TTT','966','達仁鄉'),(351,'HUA','970','花蓮市'),(352,'HUA','971','新城鄉'),(353,'HUA','972','秀林鄉'),(354,'HUA','973','吉安鄉'),(355,'HUA','974','壽豐鄉'),(356,'HUA','975','鳳林鎮'),(357,'HUA','976','光復鄉'),(358,'HUA','977','豐濱鄉'),(359,'HUA','978','瑞穗鄉'),(360,'HUA','979','萬榮鄉'),(361,'HUA','981','玉里鎮'),(362,'HUA','982','卓溪鄉'),(363,'HUA','983','富里鄉'),(364,'JME','890','金沙鎮'),(365,'JME','891','金湖鎮'),(366,'JME','892','金寧鄉'),(367,'JME','893','金城鎮'),(368,'JME','894','烈嶼鄉'),(369,'JME','896','烏坵鄉'),(370,'LJF','209','南竿鄉'),(371,'LJF','210','北竿鄉'),(372,'LJF','211','莒光鄉'),(373,'LJF','212','東引鄉');"

                execute_command(lock_zip_command)
                execute_command(zip_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.zip length: {len(zip)}")

            # current_version
            execute_command("SELECT * FROM mssp.current_version;")
            current_version = cursor.fetchall()
            if len(current_version) == 0:
                VERSION = os.getenv("VERSION") or "v2.0.2.4"
                lock_current_version_command = "LOCK TABLES `current_version` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_version_command = f"INSERT INTO `current_version` VALUES (1,'{VERSION}','{time}','{time}');"

                execute_command(lock_current_version_command)
                execute_command(current_version_command)
                execute_command(close_command)
            else:
                set_info(f"mssp.current_version length: {len(current_version)}")

            # clausetype
            execute_command("SELECT * FROM mssp.clausetype;")
            clausetype = cursor.fetchall()
            if len(clausetype) == 0:
                lock_clausetype_command = "LOCK TABLES `clausetype` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                clausetype_command = f"INSERT INTO `clausetype` (`uid`,`type_name`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('856f8d3d-8915-469a-a45b-4d1f71844db2','SEMI E187-0122','ff81c0d6-e8d2-451f-a226-935cbd913541','{time}','system','4a52eeff-1124-4dea-8444-2d8e05f06fbc','{time}','system'),('9e7226fe-8216-4ac2-a59f-ec8c4186c8d4','資通安全責任等級A級之公務機關應辦事項','e6b725ac-06cb-4caa-87ef-f6fbe296b059','{time}','system','4d76bd7c-906b-4e7f-9d88-b1620e4a68f3','{time}','system');"

                cursor.execute(lock_clausetype_command)
                cursor.execute(clausetype_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.clausetype length: {len(clausetype)}")

            # clause
            execute_command("SELECT * FROM mssp.clause;")
            clause = cursor.fetchall()
            if len(clause) == 0:
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lock_clause_command = "LOCK TABLES `clause` WRITE;"
                clause_command = f"INSERT INTO `clause` (`uid`,`clause_type_id`,`clause_title_id`,`clause_title`,`clause_subtitle`,`clause_item`,`created_id`,`created_datetime`,`created_user`,`modify_id`,`modify_datetime`,`modify_user`) VALUES ('d57780f4-72f1-4649-9cd0-7793b99aded9','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'7.2 Support for Operating System','E187.00-RQ-00001-00','Equipment supplier shall not ship equipment with OS that are not supported by the OS vendor (e.g., end of life). [/RQ]','305d8b49-61c9-46c5-9d59-5c264e88f822','{time}','system','a1945fb0-58a3-42d5-ac59-41f738d3c960','2022-10-18 14:08:09','system'),('ec7310fd-0aa3-4bca-8130-145ca43ebe75','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'7.2 Support for Operating System','E187.00-RQ-00002-00','Equipment suppliers shall provide the procedure to apply the patches or the security updates.It includes items to evaluate software compatibility, software package dependency, performance impact, and side-effect of applying the patches or security updates. [/RQ]','5586f1fb-828d-43a7-9fa5-f6b3aff9cc55','{time}','system','6f6ae114-588f-495b-a155-10cbf881444c','{time}','system'),('74bdb632-f12b-4601-b22b-da4d51447048','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'8.2 Network Transmission Security','E187.00-RQ-00003-00','Equipment that provides applications of web service, file transfer, and terminal service(telnet) shall support secure transmission protocols like HyperText Transfer Protocol Secure (HTTPS), Secure File Transfer Protocol (SFTP), and Secure Shell (SSH) accordingly. [/RQ]','717334cb-3c79-42e9-b87f-4ad023365ee0','{time}','system','c5ba760b-b963-4151-a5de-d219c7127f5f','{time}','system'),('5c9ac380-5e7b-405c-805a-1240ebc522ee','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'8.3 Network Configuration Management','E187.00-RQ-00004-00','Equipment supplier shall provide documentation for network configurations including network protocols/ports usage and provide maintenance instructions for changing the network configuration if supported (such as changing the network port assignment). [/RQ]','ba978909-8c43-4fb6-b0bf-dc088bb7cbc3','{time}','system','7f8eb032-7704-43da-9613-3ef1bb2c4ea0','{time}','system'),('3af770c6-7907-4d8b-9f0e-87c96fac56b5','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.2 Vulnerability Mitigation','E187.00-RQ-00005-00','Equipment suppliers shall perform vulnerability scan prior to equipment shipment and deliver a scanning report, including name and version of scanning tool, scanning scope of coverage, and scanning date, with evidence of no critical severity vulnerability according to common industrial vulnerability scoring standard. [/RQ]','bb050c22-77ad-4d80-8420-a4e901322302','{time}','system','4369a9d3-ba90-4311-8004-a368f3e4e103','{time}','system'),('041e037c-a0b7-4e0e-ab71-c73dbcc0ec18','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.3 Malware Scanning','E187.00-RQ-00006-00','Equipment suppliers shall perform malware scan prior to equipment shipment and deliver a scanning report, including name and version of scanning tool, scanning scope of coverage, and scanning date. [/RQ]','71816c72-30b0-4b0e-b76e-9a94c3c700e7','{time}','system','de2c1eba-4ae7-4aaf-8740-f1d4231281ae','{time}','system'),('bdc199fa-de33-46f9-a751-01c73bc7fe64','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.4 Anti-Malware Protection','E187.00-RQ-00007-00','Equipment suppliers shall provide documentation that specifies the compatible anti-malware solutions for the fab equipment. [/RQ]','7e4bfcf9-cf6b-4941-9d4b-430070ff8fcf','{time}','system','bd90ad1f-fc9f-4505-9469-f171a7c0098d','{time}','system'),('cca24e6d-f378-479f-bf3d-766acdd0a9db','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.4 Anti-Malware Protection','E187.00-RQ-00008-00','Equipment suppliers shall provide documents regarding security hardening including:• Enable/disable input/output interfaces such as Universal Serial Bus (USB) or DVD Rewritable (DVD±RW).• Disable unused operating system utilities and services.[/RQ]','63bea039-6ead-48fb-b9a0-c7f979f041de','{time}','system','677ccdac-19c1-41fb-86bf-ace9b87fc626','{time}','system'),('6c7720dc-c305-4b43-a8c6-fe1460b2c802','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.5 Access Control Mechanism','E187.00-RQ-00009-00','Authentication mechanism(s) shall be used for operating system and equipment access control. [/RQ]','d87920ba-d683-42b7-8e43-6372ffd67abc','{time}','system','4a972d8e-c113-41e9-9c58-bec6af4f3721','{time}','system'),('59965c43-850f-4f46-b0ba-07cb39adfa6e','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'9.5 Access Control Mechanism','E187.00-RQ-00010-00','Equipment suppliers shall provide access rights/privileges authorization solutions to support segregation of duties and least privilege policy. [/RQ]','2f5e06c2-571b-4f7e-8d89-4b77609b42a2','{time}','system','f76b1343-7a0e-4ae4-9e06-135eeba5d087','{time}','system'),('97eafe4b-ffde-4550-b2aa-1b168bb24b0a','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'10.2 Log Requirement','E187.00-RQ-00011-00','Fab equipment shall be capable of recording and exporting system and application security event logs. [/RQ]','8d784244-119f-4f9e-9c67-e1b3284546b8','{time}','system','8ee1b8b4-8144-4fe8-89ee-928ac43e5f99','{time}','system'),('73aaa761-f59b-434a-b842-5087de68b0a5','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'10.2 Log Requirement','E187.00-RQ-00012-00','The types of event logs shall include access control, configuration changes and system errors, and the event log consists of event type, event description, user account and timestamp. [/RQ]','181a5829-94ef-4ad4-b2a1-82c6f52ce5f8','{time}','system','a757a4f1-2af0-4f99-87f7-012358d47575','{time}','system'),('c6598ac1-a73b-4ee1-b84d-af3176f73a53','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90001-00','Each party of the capabilities defined in this specification shall document compliance to E187.00 capability requirements per with Table A1-1 the following compliance codes: C – comply, NC – not comply, NA – not applicable. [/RQ]','12834b86-cd23-4cea-be02-ab7f3bd0485c','{time}','system','776cd7fb-4aba-4149-8b5e-982d2cce2319','{time}','system'),('28b7c6b2-792f-4085-a550-31d1ff458dcd','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90002-00','The NA compliance code shall be used only in the case where a requirement is conditional and the condition evaluates to render the requirement not applicable for the current implementation. [/RQ]','3c7dc65c-920d-427c-aaf5-acf9ae84bfd2','{time}','system','071667b3-0b23-4be9-9e34-df486bf68979','{time}','system'),('935231b3-749c-4b1d-900d-73a3944d249a','856f8d3d-8915-469a-a45b-4d1f71844db2',NULL,'A1-1 Compliance Table: Capability Requirements','E187.00-RQ-90003-00','An explanation for NC shall be provided by the party. [/RQ]','33c28e38-2243-4c78-b21a-b456c7bd2ebf','{time}','system','b1dfc804-14a5-40cb-a83c-c8bf378cfb15','{time}','system'),('61959ed6-edc1-44f4-8ed8-9ab55e418fe3','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通系統分級及防護基準','資通系統分級及防護基準 ','初次受核定或等級變更後之一年內，針對自行或委外開發之資通系統，依附表九完成資通系統分級，並完成附表十之控制措施；其後應每年至少檢視一次資通系統分級妥適性。','122b5742-dcbd-4b5a-923d-17c3eb70f018','{time}','system','a6e13ac0-d0a5-4da0-b849-60f6dd9cf26f','{time}','system'),('11671c1e-ee2f-4b55-bde5-2b062f47497d','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資訊安全管理系統之導入及通過公正第三方之驗證','資訊安全管理系統之導入及通過公正第三方之驗證','初次受核定或等級變更後之二年內，全部核心資通系統導入CNS 27001資訊安全管理系統國家標準、其他具有同等或以上效果之系統或標準，或其他公務機關自行發展並經主管機關認可之標準，於三年內完成公正第三方驗證，並持續維持其驗證有效性。','3dbb6042-146e-4727-b6c1-84cae223685f','{time}','system','a5799b93-57ec-4398-a369-67254453df1b','{time}','system'),('6fa78846-585d-41d7-b71d-4f45cc17eb2e','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專責人員','資通安全專責人員','初次受核定或等級變更後之一年內，配置四人；須以專職人員配置之。','62a6ebab-41b3-49e9-b01a-25be916302a3','{time}','system','c6316708-397e-4e64-9e8b-c578a0c447b7','{time}','system'),('3dae48aa-c36a-4635-a2c6-e4648a2b0638','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'內部資通安全稽核','內部資通安全稽核','每年辦理二次。','eb422060-7c89-4857-9bdc-10383bf1ab3a','{time}','system','ab8454f2-fa4b-4060-a000-5772a2769401','{time}','system'),('7a754f60-37c6-4786-b2e3-19b931595af9','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'業務持續運作演練','業務持續運作演練','全部核心資通系統每年辦理一次。','38608f91-09c8-4b7e-a05d-80cfd6fe2600','{time}','system','7a2a2787-5c05-49ed-986e-10aad37d42b8','{time}','system'),('771ec034-c653-4182-9e83-9cf867e303ab','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資安治理成熟度評估','資安治理成熟度評估','每年辦理一次。','287db92c-1c21-429a-b5cb-693d929266b9','{time}','system','3c427654-54d2-4e8f-ada3-358ce4646df9','{time}','system'),('3700cb99-1310-44b9-88eb-38f38efd7ee2','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'安全性檢測','網站安全弱點檢測','全部核心資通系統每年辦理二次。','0a88b1fc-a517-4083-913e-a8dfe747fb9d','{time}','system','b741f611-e93a-4b96-9126-89b047f35054','{time}','system'),('a7745c90-c989-4854-88f0-eff21280b7f9','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'安全性檢測','系統滲透測試','全部核心資通系統每年辦理一次。','383b1343-1568-4d16-a185-e23ac61596f6','{time}','system','d2698316-24d2-43f5-97c9-07feca86f859','{time}','system'),('43bed624-bf8a-479b-9784-1c80996d997f','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','網路架構檢視','每年辦理一次。','22a234e0-3954-4820-b7c7-92e5a8a0d9ef','{time}','system','ed73a3c9-48ce-43fa-8693-d21cebc81015','{time}','system'),('a3c42146-3849-402a-b12a-2fbf8089f9fd','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','網路惡意活動檢視','每年辦理一次。','fea4a04e-64c4-4a59-b115-d729e613e285','{time}','system','3da5bcda-716f-4171-8b4f-a44979948cf7','{time}','system'),('81b57bb9-b51f-45e2-9eca-57acf79f647a','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','使用者端電腦惡意活動檢視','每年辦理一次。','060dc205-d8f2-46c3-994f-5bc0365d1c7e','{time}','system','c56fa6ec-c6cb-4d9e-83e9-36d37aa02452','{time}','system'),('b45e9300-868c-4c65-aa2b-2cca1c8e5a34','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','伺服器主機惡意活動檢視','每年辦理一次。','c0de9794-a958-4b22-a5c7-674b197277b0','{time}','system','9d762f84-4ecf-471d-be33-9d8aee07ad5e','{time}','system'),('add4e343-c360-4248-a6ca-8ca1f16c2ed4','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全健診','目錄伺服器設定及防火牆連線設定檢視','每年辦理一次。','80e7fe26-14e5-41b4-ba6e-d4b85281203d','{time}','system','e810a320-23c1-4393-b64f-1957840eb973','{time}','system'),('70cc966a-75ef-433a-9736-27a7c5cd6517','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全威脅偵測管理機制','資通安全威脅偵測管理機制','初次受核定或等級變更後之一年內，完成威脅偵測機制建置，並持續維運及依主管機關指定之方式提交監控管理資料。','e8dcd84b-2f50-4d0e-8e7b-1335f42334c9','{time}','system','720b2f6b-0419-4bbb-84b1-42facc6db016','{time}','system'),('38587d52-1a66-4d0b-bd6f-00cf2870a5d2','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'政府組態基準','政府組態基準','初次受核定或等級變更後之一年內，依主管機關公告之項目，完成政府組態基準導入作業，並持續維運。','fd027a1d-e0fe-4f71-b68a-5e04322e32aa','{time}','system','09b06c01-89a4-4c22-a0cb-becc851dae67','{time}','system'),('2e2aaaf7-9b68-4f44-8f3b-1d2ff5ad5c53','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','防毒軟體','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','ed8b5dc3-1d83-482e-ac96-f565983e0c4d','{time}','system','fe787f90-7184-4b90-b5a8-a72c860305a3','{time}','system'),('b30cc9c7-d58a-48dd-ab5e-6914824eb3c7','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','網路防火牆','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','4d7a00f0-7c67-4d64-83fa-d8d2905a05b2','{time}','system','be14e698-726c-4fba-94cf-ea5c7ca69d3b','{time}','system'),('cfae0471-3c75-44c8-98b1-a28b5cb06c5a','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','具有郵件伺服器者，應備電子郵件過濾機制','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','6407b66f-b3b8-4b5f-9c62-bbaed6a2e203','{time}','system','b3881359-a2e0-4aad-99fe-b5c0ab148f2d','{time}','system'),('c0b7c185-6109-4866-ac52-cb63fbcb2ab1','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','入侵偵測及防禦機制','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','8029fa0a-e421-47dc-b389-99b05a834025','{time}','system','8ae095a3-fc46-4f44-b003-74a2dc878141','{time}','system'),('ecdbc255-2959-4a9a-ae42-66b0b14b6807','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','具有對外服務之核心資通系統者，應備應用程式防火牆','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','7f24f636-7559-4e38-9ba7-54c106bd1e8d','{time}','system','9b3beb0c-95ae-4e3d-a6af-6d0cf89fe186','{time}','system'),('d874eefc-7241-4b85-926a-01f10de0edc8','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全 防護','進階持續性威脅攻擊防禦措施','初次受核定或等級變更後之一年內，完成各項資通安全防護措施之啟用，並持網路防火牆 具有郵件伺服器者，應備電子郵件過濾機制入侵偵測及防禦機制具有對外服務之核心資通系統者，應備應用程式防火牆進階持續性威脅攻擊防禦措施續使用及適時進行軟、硬體之必要更新或升級。','8a2990a3-b4bb-4cc3-8a23-939929099ef0','{time}','system','b49c35a4-401e-4b3b-ad9d-b33ddd7ac399','{time}','system'),('6004d073-f11f-4357-b504-62ee4c1a9ca6','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全教育訓練','資通安全及資訊人員','每年至少四名人員各接受十二小時以上之資通安全專業課程訓練或資通安全職能訓練。','659103a2-c10d-42b8-a2b3-dd34ecb199b2','{time}','system','45e911a9-9eec-487b-9dbc-3db2e9cd7304','{time}','system'),('c01fb734-e041-4380-8bc3-bfada84f21c5','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全教育訓練','一般使用者及主管','每人每年接受三小時以上之一般資通安全教育訓練。','55b727c3-d673-40f6-a3ff-1392f266cf96','{time}','system','14a5c720-19d3-40b3-9cfb-f4ffbcc720ee','{time}','system'),('02d09ed9-b3c6-438f-8538-86f020c3b3c4','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專業證照及職能訓練證書','資通安全專業證照','初次受核定或等級變更後之一年內，資資通安全專業證照及職能訓練證書資通安全專業證照資通安全職能評量證書通安全專職人員總計應持有四張以上並持續維持證照之有效性。','24eab8f1-e527-46d8-8cbd-a6f76cfe18c9','{time}','system','b87a20ad-8fa5-439e-8c1a-ff2d427b30d4','{time}','system'),('28b98dbf-8ee9-49e9-88ed-1273aa269e59','9e7226fe-8216-4ac2-a59f-ec8c4186c8d4',NULL,'資通安全專業證照及職能訓練證書','資通安全職能評量證書','初次受核定或等級變更後之一年內，資通安全專職人員總計應持有四張以上並持續維持證書之有效性','2e16c4c9-2fcd-4638-842e-3e44061ef0fb','{time}','system','9fb72456-078a-4f88-991b-99cc0195a991','{time}','system');"

                cursor.execute(lock_clause_command)
                cursor.execute(clause_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.clause length: {len(clause)}")

            # api
            execute_command("SELECT * FROM mssp.api;")
            api = cursor.fetchall()
            if len(api) == 0:
                lock_api_command = "LOCK TABLES `api` WRITE;"
                api_command = "INSERT INTO `api` (`id`,`name`,`url`) VALUES (1,'LOGIN','/login'),(2,'REFRESH','/refresh'),(3,'LOGOUT','/logout'),(4,'INCIDENTS','/incidents'),(5,'INCIDENT','/incident'),(6,'INCIDENT','/incidents/archive'),(7,'ACCIDENTS','/accidents'),(8,'ACCIDENT','/accidents'),(9,'ACCIDENT','/accident'),(10,'ACCIDENT','/accidents/archive'),(11,'ACCIDENT','/accident/verify/submit'),(12,'ACCIDENT','/verify/reject'),(13,'ACCIDENT','/verify/signature'),(14,'ACCIDENT_VERIFY','/accidents/verify'),(15,'ACCIDENT_FLOWS','/accident/verify-flows'),(16,'ACCIDENT_FLOWS','/accident/verify-flows/menu'),(17,'ACCIDENT_FLOW','/accident/verify-flow'),(18,'ORGANIZATIONS','/submit/organizations/menu'),(19,'ORGANIZATION','/configure/organization'),(20,'NOTIFICATION','/configure/notification/incident'),(21,'REPORTS','/reports/menu'),(22,'REPORT','/report'),(23,'SCHEDULES','/report/schedules'),(24,'SCHEDULE','/report/schedule'),(25,'DEVICES','/devices'),(26,'DEVICES','/devices/sync'),(27,'DEVICE','/devices/import'),(28,'DEVICE','/devices/import/csv'),(29,'DEVICE','/device'),(30,'DEVICE_TYPE','/global/menu/device_type'),(31,'DEVICEGROUPS','/device-groups'),(32,'DEVICEGROUPS','/device-group/menu'),(33,'DEVICEGROUP_TYPE','/global/menu/device_group_type'),(34,'DEVICEGROUP','/device-group'),(35,'SENSORS','/sensors'),(36,'SENSORS','/sensor/menu'),(37,'SENSOR_TYPE','/global/menu/sensor_type'),(38,'SENSOR','/sensor'),(39,'COMPANIES','/companies'),(40,'COMPANIES','/company/menu'),(41,'COMPANY','/company'),(42,'COMPANY','/companies/active'),(43,'USERS','/users'),(44,'USERS','/users/menu'),(45,'USER','/user'),(46,'SEND_MAIL','/mail/test'),(47,'ROLES','/roles'),(48,'ROLES','/roles/menu'),(49,'ROLE','/role'),(50,'LICENSE','/configure/license'),(51,'SMTP','/configure/smtp'),(52,'API_TOKEN','/data-migrate/api-tokens'),(53,'CITY','/city/menu'),(54,'ZIP','/zip/menu'),(55,'COLLECTIONS','/sentiments/my'),(56,'COLLECTION','/collections/create'),(57,'COLLECTION','/collections/delete'),(58,'SENTIMENTS','/sentiments'),(59,'SENTIMENT','/sentiment'),(60,'REGULATIONS','/cyberSecurity/clause/types'),(61,'CLAUSES','/cyberSecurity/clause/clausetype'),(62,'CLAUSE','/cyberSecurity/clause'),(63,'CLAUSE_FILES','/cyberSecurity/clause/file/clauseuid'),(64,'CLAUSE_FILE','/cyberSecurity/clause/file'),(65,'CLAUSE_FILE','/cyberSecurity/clause/file/download'),(66,'CLAUSE_DASHBOARD','/cyberSecurity/clause/dashboard'),(67,'RECORDS','/records'),(68,'WEB_URL','/web-url/menu'),(69,'ACCIDENT','/accident/verify/signature'),(70,'ACCIDENT','/accident/verify/reject'),(71,'REGULATION','/cyberSecurity/clause/pdfgen'),(72,'PERMISSIONS','/permissions/menu'),('73','CLAUSE_PERMISSIONS','/cyberSecurity/clause/type/permissions'),('74','USER_PROFILE','/user/profile'),('75','CLAUSE_PERMISSION','/cyberSecurity/clause/type/permission');"

                cursor.execute(lock_api_command)
                cursor.execute(api_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.api length: {len(api)}")

            # web_url
            execute_command("SELECT * FROM mssp.web_url;")
            web_url = cursor.fetchall()
            if len(web_url) == 0:
                lock_web_url_command = "LOCK TABLES `web_url` WRITE;"
                web_url_command = "INSERT INTO `web_url` (`id`,`name`,`url`) VALUES (1,'Login','/'),(2,'SecurityEventManage','/security/incident-manage'),(3,'SecurityAlarmManage','/security/accident-manage'),(4,'SecurityAlarmVerify','/security/accident-verify-manage'),(5,'SubordinateManage','/configure/subordinate'),(6,'AlarmConfigManage','/configure/accident-submit'),(7,'EmailNotificationManage','/configure/notification'),(8,'StatisticsReportManage','/report/statistics-report'),(9,'ScheduleReportManage','/report/schedule-report'),(10,'DeviceManage','/asset/device-manage'),(11,'DeviceGroupManage','/asset/device-group'),(12,'SensorManage','/asset/sensor-manage'),(13,'CompanyManage','/company/company-manage'),(14,'UserManage','/user/user-manage'),(15,'RoleManage','/user/role-manage'),(16,'SystemConfigManage','/configure/system'),(17,'MailServerManage','/configure/smtp'),(18,'LicenseConfigManage','/configure/license'),(19,'AuditManage','/audit/audit-manage'),(20,'RecordManage','/configure/record-manage'),(21,'PulseCreateManage','/pulses/create-manage'),(22,'SentimentManage','/pulses/sentiment-manage'),(23,'UserManage','/user/profile');"

                cursor.execute(lock_web_url_command)
                cursor.execute(web_url_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.web_url length: {len(web_url)}")

            # information category
            execute_command("SELECT * FROM mssp.information_category;")
            information_category = cursor.fetchall()
            if len(information_category) == 0:
                lock_information_category_command = "LOCK TABLES `information_category` WRITE;"
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                information_category_command = f"INSERT INTO `information_category` (`id`,`uid`,`information_category`,`modify_datetime`,`created_datetime`,`content_description`,`intelligence_theme_example`) VALUES (1,'a4978b0c-c9e0-44cc-bfec-3ca35e30758d','惡意內容','{time}','{time}','針對透過文字、照片、影片等形式散播不當內容之情資','外部使用者對多個客戶使用者寄送 SPAM 信件'),(2,'6cc95721-2bdb-4c5b-b6c1-b6d42ebce058','惡意程式','{time}','{time}','針對與相關惡意程式之情資','後門/間諜程式連線,內部主機疑似進行惡意程式連線,惡意程式下載行為'),(3,'f329226e-5e91-44dc-8dd1-76d81fb2e278','資訊蒐集','{time}','{time}','針對透過掃描、探測及社交工程等攻擊手法取得資訊之情資','外部主機執行掃描探測攻擊,弱點掃描行為'),(4,'fe9f04fe-a22e-4e0f-91f9-7dd37459d115','入侵嘗試','{time}','{time}','針對嘗試入侵未經授權(Authorization)主機之情資','密碼猜測行為,密碼暴力破解,特權帳號使用非允入 IP,登入事件,非上班時間任何登入嘗試'),(5,'223cb8d9-d587-43da-a0df-abdf1eecd956','入侵攻擊','{time}','{time}','針對系統遭未經授權(Authorization)存取或取得系統/使用者權限之情資','內部電腦連線至 C&C網站,內部主機單次連線至惡意 IP,網頁遭受竄改'),(6,'dee17eee-c053-498e-b568-98b2dac68a36','服務阻斷','{time}','{time}','針對影響服務可用性(Availability)或造成服務中斷之攻擊情資','外部主機疑似進行阻斷服務攻擊,重要系統疑似遭受阻斷服務攻擊,電子申請服務異常,設備服務終止'),(7,'8caa8cc2-3887-45dc-927c-ce6a36b94623','資訊內容安全','{time}','{time}','針對系統遭未經驗證(Authentication)存取或影響資訊機敏性(Confidentiality)之情資','資料外洩攻擊,應用程式存取 DB,新增刪除資料異動'),(8,'a3e98d25-6ed2-4c0f-a7f1-cb56480c1ef2','詐欺攻擊','{time}','{time}','針對偽冒他人身分、系統服務及組織等進行攻擊行為之情資','發送釣魚郵件'),(9,'6b199b8d-b11b-4f22-98a5-5cb38eb897bd','系統弱點','{time}','{time}','針對系統存在弱點之情資,可能遭利用進而影響系統機敏性(Confidentiality)、完整性(Integrity)或可用性(Availability),分享相關資訊予特定會員','系統疑似存在 RCE 漏洞'),(10,'b088fab9-97a9-440b-a68d-d1380701578c','其他','{time}','{time}','分享非屬前9項之情資','無');"

                cursor.execute(lock_information_category_command)
                cursor.execute(information_category_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.information_category length: {len(information_category)}")

            # kill chain stage
            execute_command("SELECT * FROM mssp.kill_chain_stage;")
            kill_chain_stage = cursor.fetchall()
            if len(kill_chain_stage) == 0:
                lock_kill_chain_stage_command = "LOCK TABLES `kill_chain_stage` WRITE;"
                kill_chain_stage_command = "INSERT INTO `kill_chain_stage` (`id`,`uid`,`stage`) VALUES (1,'ff327b0e-8bde-43c3-a67c-15cfc1bcf76a','Reconnaissance'),(2,'499c27d4-b0cb-4fc0-897a-be639403b6b6','Weaponization'),(3,'d1680c70-16c9-4952-a54c-9185c25a71be','Delivery'),(4,'271b15fc-6283-4eb1-a58d-ec3c8cd8f165','Exploitation'),(5,'87c30267-43bd-4a13-9b66-926a202f701e','Installation'),(6,'61e7eaac-3381-46fa-9916-b1f0a41877ab','Command-Control'),(7,'fee17450-c982-4d82-b56c-bc57be2a0529','Actions');"

                cursor.execute(lock_kill_chain_stage_command)
                cursor.execute(kill_chain_stage_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.kill_chain_stage length: {len(kill_chain_stage)}")

            # unit_information
            execute_command("SELECT * FROM mssp.unit_information;")
            unit_information = cursor.fetchall()
            if len(unit_information) == 0:
                lock_unit_information_command = "LOCK TABLES `unit_information` WRITE;"
                unit_information_command = "INSERT INTO `unit_information` (`id`,`uid`,`type`,`description`) VALUES (1 ,'7c5075b6-35db-4d2f-b793-3fe8bfed9ed2','individual','A single person.e'),(2 ,'935abd69-bf3e-4856-af88-86bfddd2be02','group','An informal collection of people, without formale governance, such as a distributed hacker group.'),(3 ,'0d296693-38c8-47d7-830f-198bad8da8db','system','A computer system, such as a SIEM'),(4 ,'72b3f06f-9437-475b-8a5a-783b2678bf5b','organization','A formal organization of people, with governance, such as a company or country.'),(5 ,'d67d2846-c6c1-497d-bb09-8ca5de828021','class','A class of entities, such as all hospitals, all Europeans, or the Domain Administrators in a system.'),(6 ,'60a19066-1930-41aa-aa36-48a6f0599b65','unspecified','It is unspecified (or unknown) whether the classification is an individual, group, system, organization, or class.'),(7 ,'5eeb90ad-befa-40be-91a0-677954d2426a','SOC','技服中心定義 for 資安監控單位'),(8 ,'e36fb5ad-b72a-4c5c-9d8b-bb7bee977003','government','技服中心定義 for 受駭單位');"

                cursor.execute(lock_unit_information_command)
                cursor.execute(unit_information_command)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.information_category length: {len(information_category)}")

            # stix_roles
            execute_command("SELECT * FROM mssp.stix_roles;")
            stix_roles = cursor.fetchall()
            if len(stix_roles) == 0:
                lock_stix_roles_command = "LOCK TABLES `stix_roles` WRITE;"
                unit_stix_roles = "INSERT INTO `stix_roles` (`id`,`uid`,`role_type`,`roles`) VALUES (1 ,'6cef4433-7930-4143-b3d2-f24b4adc239e','單位等級','A'),(2 ,'b67f089a-eb0d-4f7a-80c9-76853889f65a','單位等級','B'),(3 ,'0a19a487-4265-4721-9c5a-a04a9b2564f8','單位等級','C'),(4 ,'c1e5572d-6eea-4991-87b3-9e21e4a20730','單位等級','D'),(5 ,'a14b6d8f-247d-4c55-9972-122a9bf040f6','單位等級','E'),(6 ,'76c67782-9b1e-41d5-a1b0-ba9328d91caf','資安防護類型','防毒軟體'),(7 ,'fecbb22e-0274-46aa-a867-3c155b1b831c','資安防護類型','電子郵件過濾機制'),(8 ,'dc3bdb89-411d-4889-8318-bdf1cc5ecc58','資安防護類型','應用程式防火牆'),(9 ,'cf62f285-5c1c-4fd0-884a-4d22062cddea','資安防護類型','網路防火牆'),(10,'6ee31978-f449-4827-89e0-8d004b9ad22d','資安防護類型','入侵偵測及防禦機制'),(11,'f087a26b-3df0-40c7-b1e4-6d31fe4e5b70','資安防護類型','進階持續性威脅攻擊防禦措施'),(12,'2047c0df-3a8c-4ac1-9bfd-da7c32f9de6a','資安防護類型','端點偵測及應變機制'),(13,'5bc8fc54-1355-431d-8d74-15562eca9879','資安防護類型','目錄服務系統'),(14,'7c0aa4f9-7855-4a0e-abef-fb2cc93d135c','資安防護類型','核心資通系統');"

                cursor.execute(lock_stix_roles_command)
                cursor.execute(unit_stix_roles)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.information_category length: {len(stix_roles)}")

            # unit_region
            execute_command("SELECT * FROM mssp.unit_region;")
            unit_region = cursor.fetchall()
            if len(unit_region) == 0:
                lock_unit_region_command = "LOCK TABLES `unit_region` WRITE;"
                unit_unit_region = "INSERT INTO `unit_region` (`id`,`uid`,`industry_sector`,`description`) VALUES (1 ,'7f263081-dba7-4b2a-8832-77a4f29b52d6','agriculture',''),(2 ,'80ea9648-2d19-43db-a0f9-25a8f9425a6f','aerospace',''),(3 ,'4f9902dc-3b88-4a27-9edf-e6b9428d540c','automotive',''),(4 ,'b8eec846-4db1-4894-bfbe-09b1e4464a95','communications',''),(5 ,'a67b956a-2c46-4771-a655-173a887a33f7','construction',''),(6 ,'63527713-01fa-4536-902e-ef1ea49a73d1','defence',''),(7 ,'1227f756-1d50-4059-98e4-e162c9c6d772','education',''),(8 ,'a5448161-a3a6-4e6e-96f2-863f16ee10fc','energy',''),(9 ,'e954f09b-9ea6-42e2-8c38-003a4f838e0e','entertainment',''),(10,'eac0d410-8e91-4290-b305-36355ca4f573','financial-services',''),(11,'cbad7671-5b6f-49de-b178-18d8dde0ed10','government-national',''),(12,'5d2960a3-d3ef-4701-9462-6c4f1e3414ce','government-regional',''),(13,'21f13d2b-beb0-47a3-b20b-adbc91d09b51','government-local',''),(14,'ab851131-db9a-40ab-a657-e16c127d3e0d','government-public-services','emergency services,sanitation'),(15,'ff65f1b4-4313-4f68-869a-df6278d25a79','healthcare',''),(16,'a345f519-e3ee-4f07-a40b-f099eb16b005','hospitality-leisure',''),(17,'7f3158d9-f9d4-47a3-89a2-9c186dfd37fb','infrastructure',''),(18,'d73db6ab-e621-42bb-afd9-087689d52be4','insurance',''),(19,'d94a3695-3d31-42d8-b9ea-96a87c3eefbc','manufacturing',''),(20,'0f514524-3eed-49c0-b0a9-3248bec8f0ed','mining',''),(21,'79c65129-2e53-43c4-9772-9b559ea76661','non-profit',''),(22,'a14561e4-1238-4320-a3cb-043861e318da','pharmaceuticals',''),(23,'02d774d7-1bf9-46dd-9224-cc1c7a9a4bf1','retail',''),(24,'a3201dab-4738-41a3-a756-1cc204fe4e72','technology',''),(25,'79b07beb-1349-48b6-b302-5c7e62270222','telecommunications',''),(26,'e1383d6f-5729-49e0-aba2-ee2ea68cf884','transportation',''),(27,'9d1ed3c2-50ef-4712-9953-c2b314de4826','utilities','');"

                cursor.execute(lock_unit_region_command)
                cursor.execute(unit_unit_region)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.information_category length: {len(unit_region)}")

            # identity type
            execute_command("SELECT * FROM mssp.identity_type;")
            identity_type = cursor.fetchall()
            if len(identity_type) == 0:
                lock_identity_type_command = "LOCK TABLES `identity_type` WRITE;"
                unit_identity_type = "INSERT INTO `identity_type` (`id`,`uid`,`type`) VALUES (1 ,'4f09ee98-2407-4089-9f86-59218f13d7a7','hacked unit'),(2 ,'e13359de-f81e-4161-b804-6b781f17c633','monitoring unit'),(3 ,'12fec8f0-c2ae-4b04-a276-7b84b27964e2','Information security equipment');"

                cursor.execute(lock_identity_type_command)
                cursor.execute(unit_identity_type)
                cursor.execute(close_command)
            else:
                set_info(f"mssp.information_category length: {len(identity_type)}")

            set_info("=======END SETTING DEFAULT DATA======")
            print("initdata: DONE")
    except Exception as e:
        set_info(e)
        print(e)

    cursor.close()
    conn.close()

    set_info("CLOSE CONNECTION")