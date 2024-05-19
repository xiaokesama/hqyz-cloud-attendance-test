import os
import sys

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# 日志配置
LOG_CONFIG = {
    'name': 'test123',
    'filename': os.path.join(ROOT_DIR, 'logs/test123.log'),
    'mode':'a',
    'encoding':'utf-8',
    'debug':True
}

# 储存用例的表格
CASE_TABLE = os.path.join(ROOT_DIR, 'datas/case_table.xlsx')

# 测试报告的路径
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')

# 错误截图的路径
ERROR_SCREENSHOT_PATH = os.path.join(ROOT_DIR, 'screen_shot')

# 测试用例路径
TEST_CASE_DIR = os.path.join(ROOT_DIR, 'testcases')
