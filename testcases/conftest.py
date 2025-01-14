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


def pytest_addoption(parser):
    parser.addoption("--case_id", action="store", default=None, help="Case ID to run")


def get_captcha_code(page):
    url = page.ele("xpath://*[@class='user-layout-login ant-form ant-form-horizontal']//img").attr('src')
    binary_data = base64.b64decode(url[22:])
    img = Image.open(BytesIO(binary_data))
    code = pytesseract.image_to_string(img, lang='chi_sim+eng').replace(' ', '')
    return code


def login(page):
    page.get(settings.MAIN_URL)
    sleep(2)
    page.set.window.maximized()
    sleep(2)
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
    login(page)
    yield page
    # page.quit()


# 每个case都从主页出发
@pytest.fixture
def main_page(page):
    page.get(settings.MAIN_URL)
    # page.get("https://www.baidu.com")
    yield page
