import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.base import Page
import pytest


# 提供driver给测试用例
@pytest.fixture(scope='class')
def page():
    page = Page()
    # 这里写登陆页面

    yield page
    page.quit()


# 每个case都从主页出发
@pytest.fixture
def main_page(page):
    page.get('https://www.baidu.com/')
    yield page
    page.get('https://www.baidu.com/')