import os
import sys

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# 本机IP地址和端口
LOCAL_IP = '127.0.0.1:9999'

# 网页地址
IP_ADDRESS = 'https://172.168.80.53/'
LOGIN_URL = IP_ADDRESS + 'user/login'
MAIN_URL = IP_ADDRESS + 'dashboard/analysis'

# 账号密码
USER_INFO = {
    'username': 'autoTest',
    'password': 'xk123456'
}

# 日志配置
LOG_CONFIG = {
    'name': 'test123',
    'filename': os.path.join(ROOT_DIR, 'logs/test123.log'),
    'mode':'a',
    'encoding':'utf-8',
    'debug':True
}

# sqlite数据库路径
SQLITE_DB_PATH = os.path.join(ROOT_DIR, 'datas/test.db')

# 储存用例的表格
CASE_TABLE = os.path.join(ROOT_DIR, 'datas/cases.xlsm')

# 测试报告的路径
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')

# 错误截图的路径
ERROR_SCREENSHOT_PATH = os.path.join(ROOT_DIR, 'screen_shot')

# 测试用例路径
TEST_CASE_DIR = os.path.join(ROOT_DIR, 'testcases')

MYSQL_CONFIG = {
    'host': "172.168.4.119",
    'user': "xiaoke",
    'password': "1193274986xk",
    'database': "hqzy_attendance",
    'charset': 'utf8'
}


