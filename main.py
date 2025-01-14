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

    # 获取 -m 选项
    arg = get_opts('-m')
    if arg:args.insert(0,'-m={}'.format(arg))

    # 获取 --browser 选项
    arg = get_opts('--browser')
    if arg:args.insert(0,'--browser={}'.format(arg))

    # 获取 --case_id 选项
    case_id = get_opts('--case_id')
    if case_id:
        args.append('--case_id={}'.format(case_id))
        if not arg:args.insert(0, '-m=one')


    print(args)
    pytest.main(args)
    os.system('allure generate ./reports/temp -o ./reports/report --clean')

# 运行命令示例：python main.py -m normal
# 运行命令示例：python main.py --case_id "002"
