import settings
from common.log_handler import get_logger
from common.read_xls import ReadXlsx
from settings import CASE_TABLE
from common.read_sqlite import Location, LocationManager

# 日志
logger = get_logger(**settings.LOG_CONFIG)

# 用例读取
upload_cases = ReadXlsx(CASE_TABLE).read_cases("录入")
normal_cases = ReadXlsx(CASE_TABLE).read_cases()
clean_cases = ReadXlsx(CASE_TABLE).read_cases("清除")
all_cases = ReadXlsx(CASE_TABLE).read_cases("all")
single_case = ReadXlsx(CASE_TABLE).read_cases("单个")

# 游标读取
loc = Location(settings.SQLITE_DB_PATH).get_data()

manager = LocationManager()
