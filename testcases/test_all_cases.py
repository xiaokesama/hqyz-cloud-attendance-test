import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from playwright.sync_api import sync_playwright
from common.base import ActionExecutor
from utils.read_yaml import YamlUtil


@pytest.mark.sus
@pytest.mark.parametrize("test_case", YamlUtil("datas/login_data.yaml").read_yaml())
def test_execute_actions(test_case):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        executor = ActionExecutor(page)

        actions = test_case["actions"]
        executor.execute(actions)

        context.close()
        browser.close()

# 这里多写几个test_execute_actions就并行化了