# from app.enum.code_enum import ConfigGroupCode
# from app.service.config_service import get_group_config
#
# todo_incident_notify_config = get_group_config(ConfigGroupCode.NOTIFICATION_INCIDENT.value)
# todo_incident_notify_interval = todo_incident_notify_config["interval"]

JOBS = [
    # 排程報表
    {
        # 每日凌晨1點執行統計日報，統計範圍為前一日00:00:00~23:59:59
        'id': 'DailyReport',
        'func': 'app.task.report_schedule:run_schedule_report',
        'args': ["daily"],
        'trigger': 'cron',
        'hour': 1
    },
    {
        # 每週一凌晨2點執行統計週報，統計範圍為上週一到日
        'id': 'WeeklyReport',
        'func': 'app.task.report_schedule:run_schedule_report',
        'args': ["weekly"],
        'trigger': 'cron',
        'day_of_week': 'mon',
        'hour':2
    },
    {
        # 每月一日凌晨3點執行統計月報，統計範圍為上個月1號~31(30)號
        'id': 'MonthlyReport',
        'func': 'app.task.report_schedule:run_schedule_report',
        'args': ["monthly"],
        'trigger': 'cron',
        'day': 1,
        'hour': 3
    },
    # 排程通知
    # 通知未處理資安事件
    {
        # 每N分鐘執行檢查todo通知
        'id': 'IncidentTodoNotification',
        'func': 'app.task.todo_notify_schedule:incident_todo_notify_handler',
        'trigger': 'interval',
        'minutes': 30
    },
    # 通知待審核通報單
    {
        # 每N分鐘執行檢查todo通知
        'id': 'AccidentTodoNotification',
        'func': 'app.task.todo_notify_schedule:accident_todo_notify_handler',
        'trigger': 'interval',
        'minutes': 30
    },
    # truncate user_operation_record
    {
        # 每個月 1號 truncate user_operation_record
        'id': 'TruncateUserOperationRecordTable',
        'func': 'app.task.truncate_table_schedule:truncate_table_handler',
        'trigger': 'cron',
        'day': 1,
        'hour': 4
    }
    # 更新Tips server 數據
    # {
    #     'id': 'TipsDataStatsQuery',
    #     'func': 'app.task.tips_query_schedule:tips_stats_query_handler',
    #     'trigger': 'cron',
    #     'hour': 9,
    #     'minute': 35
    # },
]
