# 命令行加在这里
import sys
import pytest
import settings
import os


def get_opts(name):
    # 如果是 --case_id 选项，则获取后面的多个用例编号
    if name == '--case_id' and name in sys.argv:
        index = sys.argv.index('--case_id')
        result = []
        for arg in sys.argv[index+1:]:
            if arg.startswith('-'):
                break
            else:
                result.append(arg)
        return '&'.join(result)
    # 如果是 --sheet 选项，则获取后面的sheet名称
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
    arg = get_opts('--case_id')
    if arg:
        args.append('--case_id={}'.format(arg))

    # 获取 --sheet 选项
    arg = get_opts('--sheet')
    if arg:
        args.append('--sheet={}'.format(arg))
        # if not get_opts('-m'):
        #     args.insert(0, '-m=sheet')

    print(args)
    pytest.main(args)
    os.system('allure generate ./reports/temp -o ./reports/report --clean')

# 运行命令示例：python main.py
# 运行命令示例：python main.py --case_id "002" "001"
# 运行命令示例：python main.py --sheet "执行"
# 运行命令示例：python main.py --sheet "执行" --case_id "002"
