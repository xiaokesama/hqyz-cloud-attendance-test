import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.base import Page
import pytest
import base64
import pytesseract
from PIL import Image
from io import BytesIO
from settings import USER_INFO,LOGIN_URL,MAIN_URL
from time import sleep


def get_captcha_code(page):
    url = page.ele("xpath://*[@class='user-layout-login ant-form ant-form-horizontal']//img").attr('src')
    binary_data = base64.b64decode(url[22:])
    img = Image.open(BytesIO(binary_data))
    code = pytesseract.image_to_string(img, lang='chi_sim+eng').replace(' ', '')
    return code


def login(page):
    page.get(MAIN_URL)
    sleep(2)
    while "/dashboard/analysis" not in page.url:
        page.get(LOGIN_URL)
        page.ele('xpath://*[@placeholder="请输入帐户名"]').input(USER_INFO['username'])
        page.ele('xpath://*[@placeholder="请输入密码"]').input(USER_INFO['password'])
        page.ele('xpath://*[@placeholder="请输入验证码"]').input(get_captcha_code(page))
        sleep(1)


# 提供driver给测试用例
@pytest.fixture(scope='class')
def page():
    page = Page()
    login(page)
    yield page
    page.quit()


# 每个case都从主页出发
@pytest.fixture
def main_page(page):
    page.get(MAIN_URL)
    yield page