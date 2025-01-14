import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.base import Page
import pytest
import base64
import pytesseract
from PIL import Image
from io import BytesIO
from DrissionPage import ChromiumPage, ChromiumOptions
import settings
from time import sleep
from common.read_xls import ReadXlsx


# 在 pytest 中添加命令行选项。这个函数用于定义可以在命令行中使用的选项。
def pytest_addoption(parser):
    # 添加 --case_id 选项
    parser.addoption("--case_id", action="store", default=None, help="Case ID to run")
    # 添加 --sheet 选项
    parser.addoption("--sheet", action="store", default=None, help="Case Sheet to run")


def get_captcha_code(page):
    url = page.ele("xpath://*[@class='user-layout-login ant-form ant-form-horizontal']//img").attr('src')
    binary_data = base64.b64decode(url[22:])
    img = Image.open(BytesIO(binary_data))
    code = pytesseract.image_to_string(img, lang='chi_sim+eng').replace(' ', '')
    return code


def login(page):
    page.get(settings.MAIN_URL)
    sleep(1)
    page.set.window.maximized()
    sleep(1)
    # 退出
    # if 'dashboard/analysis' in page.url:
    #     try:
    #         page.ele('xpath://*[@aria-label="图标: logout"]').click()
    #         page.ele('xpath://*[@class="ant-btn ant-btn-primary"]').click()
    #     except Exception as e:
    #         print(e)
    # sleep(1)
    # 登录
    while "/user/login" in page.url:
        page.ele('xpath://*[@placeholder="请输入帐户名"]').clear()
        page.ele('xpath://*[@placeholder="请输入密码"]').clear()
        page.ele('xpath://*[@placeholder="请输入验证码"]').clear()
        page.ele('xpath://*[@placeholder="请输入帐户名"]').input(settings.USER_INFO['username'])
        page.ele('xpath://*[@placeholder="请输入密码"]').input(settings.USER_INFO['password'])
        page.ele('xpath://*[@placeholder="请输入验证码"]').input(get_captcha_code(page))
        sleep(1)


# 提供driver给测试用例
@pytest.fixture(scope='class')
def page():
    co = ChromiumOptions()
    co.ignore_certificate_errors()
    co.set_address(settings.LOCAL_IP)
    page = Page(addr_or_opts=co)
    yield page
    # page.quit()


# 每个case都从主页出发
@pytest.fixture
def main_page(page):
    page.get(settings.MAIN_URL)
    yield page


@pytest.fixture(scope='class')
def get_cases(request):
    case_id = request.config.getoption("--case_id")
    sheet = request.config.getoption("--sheet")
    return ReadXlsx(settings.CASE_TABLE).get_cases(case_id, sheet)  # 返回可迭代对象


'''
pytest_generate_tests：这个钩子函数在测试函数被收集时运行，可以用于动态生成参数。
    它检查当前测试函数是否需要 case 参数，如果需要，它将调用 ReadXlsx 获取测试用例并使用 metafunc.parametrize() 来动态生成参数。
get_cases fixture：此 fixture 仍然用于获取命令行参数，但不再直接用于参数化。
'''


def pytest_generate_tests(metafunc):
    if 'case' in metafunc.fixturenames:
        get_cases = metafunc.config.getoption("--case_id")  # 获取命令行参数
        sheet = metafunc.config.getoption("--sheet")
        cases = ReadXlsx(settings.CASE_TABLE).get_cases(get_cases, sheet)
        metafunc.parametrize("case", cases)  # 动态生成参数
