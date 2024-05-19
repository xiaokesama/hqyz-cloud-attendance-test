import settings
from common.log_handler import get_logger
from common.read_xlsx import ReadXlsx
from settings import CASE_TABLE

# 日志
logger = get_logger(**settings.LOG_CONFIG)

# 用例读取
upload_cases = ReadXlsx(CASE_TABLE).get_cases("录入")
normal_cases = ReadXlsx(CASE_TABLE).get_cases()
clean_cases = ReadXlsx(CASE_TABLE).get_cases("清除")
all_cases = ReadXlsx(CASE_TABLE).get_cases("all")
