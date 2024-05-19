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
