import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from common.base import ActionExecutor
from common import upload_cases,normal_cases,clean_cases,all_cases
# 分三种：录入，执行，删除


class TestAllCases:
    @pytest.mark.parametrize("test_case", normal_cases)
    def test_execute_actions(self,test_case,main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)