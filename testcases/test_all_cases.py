import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from common.base import ActionExecutor
from common import *
from common.read_xls import ReadXlsx


class TestAllCases:

    def test_execute(self, case, main_page):
        ActionExecutor(main_page).execute(case)


