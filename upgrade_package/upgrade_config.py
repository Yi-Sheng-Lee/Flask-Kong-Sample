import subprocess
import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)


def execute_subprocess(cli):
    df = subprocess.Popen([cli], stdout=subprocess.PIPE, shell=True)
    (output, errors) = df.communicate()
    df.stdout.close()
    if errors:
        logger.error(errors)
    return output.decode().strip()


def logging_config():
    # Logging setup
    _log_level = logging.INFO

    # Logging rotate handle

    path = os.getcwd()
    log_path = f"{path}/log/upgrade/upgrade.log"

    # 若路徑不存在就新建一個
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logfile_handler = RotatingFileHandler(
        log_path,
        maxBytes=30 * 1024 * 1024,
        backupCount=5,
        encoding="UTF-8",
    )

    # Logging format handle
    logging_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logfile_handler.setFormatter(logging_format)
    logger.addHandler(logfile_handler)
    logger.setLevel(_log_level)
    return logger

