import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from common.base import ActionExecutor
from common import *
from common.read_xls import ReadXlsx


class TestAllCases:

    @pytest.mark.one
    @pytest.mark.parametrize("test_case", ReadXlsx(CASE_TABLE).read_case_by_id("001"))
    def test_execute_one(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

    @pytest.mark.all
    @pytest.mark.parametrize("test_case", all_cases)
    def test_execute_all(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

    @pytest.mark.upload
    @pytest.mark.parametrize("test_case", upload_cases)
    def test_execute_upload(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

    @pytest.mark.normal
    @pytest.mark.parametrize("test_case", normal_cases)
    def test_execute_normal(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

    @pytest.mark.clean
    @pytest.mark.parametrize("test_case", clean_cases)
    def test_execute_clean(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

    @pytest.mark.single
    @pytest.mark.parametrize("test_case", single_case)
    def test_execute_clean(self, test_case, main_page):
        executor = ActionExecutor(main_page)
        executor.execute(test_case)

