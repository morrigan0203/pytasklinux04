import subprocess
import yaml
import sys


with open('config.yaml') as f:
    data = yaml.safe_load(f)

HOST = data["HOST"]
USER = data["USER"]
PASSWD = data["PASSWD"]
USER_FOLDER = data["USER_FOLDER"]
TST_FOLDER = data["TST_FOLDER"]
OUT_FOLDER = data["OUT_FOLDER"]
FOLDER_FOLDER = data["FOLDER_FOLDER"]
COUNT = data["COUNT"]
FILE_SIZE = data["FILE_SIZE"]
ARC_TYPE = data["ARC_TYPE"]

FILE = "file.txt"
TEXT_OK = "Everything is Ok"
TEXT_FAIL = "Is not archive"
TEXT_HEADERS_ERROR = "Headers Error"


def save_log(start_time, prefix):
    with open(f'logs/{prefix}.{sys._getframe(1).f_code.co_name}.log', "a+", encoding="utf-8") as f:
        f.write(getout(f'journalctl --since "{start_time}"'))


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout and result.returncode == 0) or text in result.stderr:
        return True
    else:
        return False


def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8').stdout
