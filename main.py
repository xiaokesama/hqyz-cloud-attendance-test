# 命令行加在这里
import sys
import pytest
import settings
import os


def get_opts(name):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name)+1]


if __name__ == '__main__':
    # -m 匹配模式
    # --browser 浏览器类型
    # --alluredir 存放报告的目录

    args =['-s', '-v', '--alluredir', 'reports/temp',settings.TEST_CASE_DIR]
    arg = get_opts('-m')
    if arg:
        args.insert(0,'-m={}'.format(arg))
    arg = get_opts('--browser')
    if arg:
        args.insert(0,'--browser={}'.format(arg))
    print(args)
    pytest.main(args)
    os.system('allure generate ./reports/temp -o ./reports/report --clean')

# 运行命令示例：python main.py -m normal