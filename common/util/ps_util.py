import psutil
import platform
import subprocess
import re


def get_cpu_usage():
    return psutil.cpu_percent()


def get_mem_usage():
    return psutil.virtual_memory().percent


def get_disk_usage(path):
    if platform.system() == "Linux":
        df = subprocess.Popen(
            ['df --total -hl | grep "total"'], stdout=subprocess.PIPE, shell=True
        )
        (output, errors) = df.communicate()
        df.stdout.close()
        usage = int(
            re.search("\s(\d+)%", output.decode()).group(0).strip().split("%")[0]
        )
        return usage
    return psutil.disk_usage(path).percent
